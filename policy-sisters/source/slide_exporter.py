#!/usr/bin/env python3
"""Materialize the real SceneAgent presentation media and frozen experiment data.

Set SCENEAGENT_BASIC_AUTH only when refreshing the protected experiment.
No credentials are emitted into the deck, manifest, or browser bundle.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, os, shutil, subprocess

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT.parent
WEB = RESEARCH / 'website/public'
OUT = ROOT / 'public/joint'
DATA = ROOT / 'src/joint/data'
CACHE = ROOT / '.cache'
EXPERIMENT = 'pi05_raw_camera_sisters_20260925--0e047ee371'
ORIGIN = 'https://sceneagent.dev'
for p in (OUT, DATA, CACHE): p.mkdir(parents=True, exist_ok=True)
manifest = []

def digest(p):
    return hashlib.file_digest(p.open('rb'), 'sha256').hexdigest()

def run(args):
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL)

def film(name, source, speed=1, compress=False, poster_time=2):
    dest = OUT / 'videos' / (name + '.mp4')
    dest.parent.mkdir(exist_ok=True)
    if not dest.exists():
        if speed == 1 and not compress:
            shutil.copy2(source, dest)
        else:
            args = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source)]
            args += ['-an', '-vf', f'setpts=PTS/{speed},fps=30,scale=1280:-2', '-c:v', 'libx264', '-preset', 'fast', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(dest)]
            run(args)
    poster = dest.with_suffix('.jpg')
    if not poster.exists():
        run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', str(poster_time), '-i', str(dest), '-frames:v', '1', '-q:v', '2', str(poster)])
    probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,codec_name:format=duration','-of','json',str(dest)]))
    manifest.append({'id':name,'source':str(source),'sourceSha256':digest(source),'file':f'/joint/videos/{name}.mp4','sha256':digest(dest),'poster':f'/joint/videos/{name}.jpg','speed':speed,'duration':float(probe['format']['duration']),**probe['streams'][0]})

films = [
 ('kitchen-cover',Path.home()/'Downloads/Kitchen17_cinematic_realistic_interiors.mp4',1,False,5),
 ('kitchen', WEB/'videos/harness/codex_skills_1.mp4',1,False,5),
 ('cables', WEB/'videos/datacenter_cable.mp4',20,True,3),
 ('sunglasses', WEB/'videos/hands_sunglasses_5x.mp4',1,False,5),
 ('lab',Path.home()/'Downloads/compressed_hcrg_lab_dual_sharpa_all_fingers_front.mp4',1,False,5),
 ('codex',WEB/'videos/harness/codex_no_skills_1.mp4',1,False,2),
 ('claude',WEB/'videos/harness/claude.mp4',1,False,3),
 ('zcode',WEB/'videos/harness/zcode.mp4',1,False,3),
 ('grok',WEB/'videos/harness/grok.mp4',1,False,2),
 ('marker',WEB/'videos/sharpa_hello_world_lift_then_uncap.mp4',1,False,85),
 ('hat',WEB/'videos/liquid_death_hat_physics.mp4',1,False,18),
 ('parchment',WEB/'videos/parchment_free_fracture.mp4',1,False,60),
 ('museum',Path.home()/'Downloads/compressed_museum_destructible_cinematic_new.mp4',1,False,7),
 ('terracotta',Path.home()/'Downloads/museum_terracotta_drop_collection.mp4',1,True,4),
 ('laptop',Path.home()/'Downloads/Dexmate_Laptop_Cinematic_20261007_173402.mp4',1,True,20),
]
for args in films:
    film(*args)
    print('Ready:',args[0],flush=True)

for folder in ('marker/thumbs', 'physics-prior/hat'):
    dest=OUT/folder;dest.mkdir(parents=True,exist_ok=True)
    for source in (WEB/folder).glob('*.webp'): shutil.copy2(source,dest/source.name)
shutil.copy2(WEB/'pipeline/kitchen17_2/capture.webp', OUT/'capture.webp')
shutil.copy2(WEB/'pipeline/kitchen17_2/preview.webp', OUT/'kitchen-preview.webp')
(OUT/'branding').mkdir(exist_ok=True)
shutil.copy2(WEB/'branding/computational-robotics.jpg', OUT/'branding/computational-robotics.jpg')
shutil.copy2(RESEARCH/'website/src/content/harnessEval.json', DATA/'benchmark.json')
(OUT/'logos/harness').mkdir(parents=True,exist_ok=True)
for source in (WEB/'logos/harness').glob('*.svg'):
    (OUT/'logos/harness'/source.name).write_text(source.read_text().replace('#111111','#f2f1ed'))
marker=json.loads((WEB/'marker/scene.json').read_text())
(DATA/'marker.json').write_text(json.dumps({'cap_fit':marker['cap_fit'],'phases':marker['phases'],'measurements':marker['measurements'],'assumptions':marker['assumptions']},indent=2))

auth=os.environ.get('SCENEAGENT_BASIC_AUTH')
def fetch(url,dest):
    if not dest.exists():
        if not auth: raise RuntimeError('Set SCENEAGENT_BASIC_AUTH to refresh protected media')
        run(['curl','--fail','--silent','--show-error','--retry','2','--user',auth,'-A','Mozilla/5.0',ORIGIN+url,'-o',str(dest)])
    return dest

snapshot=CACHE/'experiment.json'
if not snapshot.exists():fetch('/api/experiments/'+EXPERIMENT,snapshot)
e=json.loads(snapshot.read_text())
objects=[{'id':o['id'],'label':o['label']} for o in e['design']['objects']]
lighting=[{'id':o['id'],'label':o['label']} for o in e['design']['lighting']]
scenes=[]
previews=OUT/'sisters';previews.mkdir(exist_ok=True)
def scene(s):
    p=fetch(s['previews']['external_left'],previews/(s['id']+'.jpg'))
    return {k:s[k] for k in ('id','label','factors','trials','pick_successes','place_successes','pick_rate','place_rate','pick_vector','place_vector','pick_wilson95','place_wilson95')} | {'preview':'/joint/sisters/'+p.name}
with ThreadPoolExecutor(max_workers=8) as pool: scenes=list(pool.map(scene,e['scenes']))
summary={k:e[k] for k in ('id','title','checkpointLabel','checkpointSha256','sceneCount','completedEpisodes','episodesPerScene','savedVideos','phase','pickRule','placeRule','updatedAt')}
summary.update(objects=objects,lighting=lighting,scenes=scenes,source=ORIGIN+'/experiments/'+EXPERIMENT)
(DATA/'sisters.json').write_text(json.dumps(summary,indent=2))
(OUT/'manifest.json').write_text(json.dumps({'clips':manifest,'branding':{'source':str(WEB/'branding/computational-robotics.jpg'),'sourceSha256':digest(WEB/'branding/computational-robotics.jpg'),'file':'/joint/branding/computational-robotics.jpg','sha256':digest(OUT/'branding/computational-robotics.jpg')},'pipeline':json.loads((OUT/'pipeline/kitchen17_2/source.json').read_text()),'experiment':{'source':summary['source'],'updatedAt':e['updatedAt'],'snapshotSha256':digest(snapshot)}},indent=2))
print('Ready: 210 actual evaluation cells and scene previews',flush=True)
subprocess.run(['python3', str(ROOT/'scripts/compress-joint-videos.py')], check=True)
