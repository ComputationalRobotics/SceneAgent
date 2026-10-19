# SceneAgent website — static export

The built, ready-to-serve copy of the SceneAgent project website
(`website/` in the research tree, a Next.js 16 static export). Everything
here is plain files: `index.html`, the `_next/` chunks and the media under
`models/`, `passes/`, `pipeline/`, `videos/`, `cousins/`,
`cousin-gallery/`, `figures/`, `branding/`. Nothing is built on GitHub's side.

Live at <https://computationalrobotics.seas.harvard.edu/SceneAgent/>.

## How it deploys

The organisation site `ComputationalRobotics/ComputationalRobotics.github.io`
carries the custom domain `computationalrobotics.seas.harvard.edu`, so every
repository in the organisation with GitHub Pages enabled is served under it at
`/<repository name>/`. The path is case-sensitive, hence the repository name
`SceneAgent`. Like the other project sites in the organisation, Pages here
publishes the `main` branch from the root folder: every push to `main` goes
live within a minute or two. `.nojekyll` keeps Jekyll from dropping the
`_next/` directory.

All URLs in the export are relative (`./_next/…`, `./models/…`), so the same
files work at `/SceneAgent/`, at a domain root or anywhere else without a
rebuild.

## Update

From `website/` in the research tree:

```bash
scripts/build_static.sh
```

That runs `next build` with `NEXT_PUBLIC_BASE_PATH=.`, verifies retained asset
hashes and the hosting size budget, and omits unused authoring assets from the
export. The full source archive remains in `website/public/`. It then syncs the
fresh export into this folder, leaving `.git`, this README, `.gitignore`,
`.nojekyll` and any `CNAME` in place. Then commit and push:

```bash
git add -A && git commit -m "Update site" && git push
```

The export is about 926 MB, including the Observatory's full-density SH3 capture,
corrected front/rear operating ropes, and exterior star sky. Its animation is
losslessly compressed. GitHub Pages sites are limited to 1 GB, so keep the
repository to this folder only; the source build rejects oversized exports.

Current source revision: `lukehollis/real2sim2real-website@24f0d3f`.

Videos and poster frames use the clean originals without the burned-in lab
watermark. The October 19 media refresh preserves all current cuts, player
URLs and the cover’s authored titles.
