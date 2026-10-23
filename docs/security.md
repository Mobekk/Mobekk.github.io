# Security and deployment

## Build and verify

Use Ruby 3.4, Bundler 2.6.9 (from Gemfile.lock), and Python 3. Install dependencies
from the lockfile; never run a copied gem executable under vendor/bundle directly.

```sh
bundle config set --local path vendor/bundle
bundle install
bundle exec bundler-audit check --update
JEKYLL_ENV=production bundle exec jekyll build --safe --strict_front_matter
python3 scripts/check_site.py _site
python3 scripts/test_templates.py
```

CI installs with `BUNDLE_FROZEN=true`. To update dependencies, run `bundle update`,
repeat all checks above, and commit Gemfile.lock. Review every dependency and action
update. Vendored dependencies and machine-specific Bundler settings are ignored.
The old dependency files were removed from Git tracking, not erased from local disk
or repository history. Reinstall into a fresh bundle directory if keeping this checkout.

For a local preview:

```sh
bundle exec jekyll serve --safe --strict_front_matter --host 127.0.0.1
```

Do not expose the development server publicly or put it behind a public proxy.
Jekyll 4.4.1 requires WEBrick; 1.9.2 is the newest published RubyGems version checked
on 2026-10-23. The upstream request-metadata issue
[ruby/webrick#198](https://github.com/ruby/webrick/issues/198) is not represented in
the Ruby advisory audit. A passing audit does not resolve that report. Watch for an
upstream release containing the fix and update the lockfile. Public GitHub Pages
serves the static artifact and does not run WEBrick.

## Activate the deployment workflow

The build moved from the GitHub Pages dependency bundle to explicit Jekyll 4
components. **Use GitHub Actions as the Pages build source**, rather than the
legacy branch builder. Legacy builds will not use this locked dependency set.

1. In [repository Pages settings](https://github.com/mobekk/mobekk.github.io/settings/pages),
   set **Build and deployment → Source → GitHub Actions**.
2. Keep the custom domain `mobekk.blog`, verify it in GitHub account Pages settings,
   retain the DNS verification TXT record, and keep **Enforce HTTPS** enabled.
3. In [environment settings](https://github.com/mobekk/mobekk.github.io/settings/environments),
   restrict the `github-pages` environment to `main`. Add required reviewers if
   desired and available for this repository/account plan.
4. Push/merge the reviewed changes to `main` or dispatch the workflow from `main`.
   Confirm the build and deployment succeed, then verify the live pages.

The workflow validates pull requests using a read-only token and no persisted Git
credentials. Only a successful push/manual run on `main` can enter the separate
Pages deployment job, which has `pages:write` and `id-token:write`. Weekly scheduled
runs audit and test but never deploy. Actions are pinned to full commit hashes;
Dependabot maintains Bundler and Actions updates. Preserve action version comments
when updating pins.

## Repository and account settings requiring owner access

These have not been changed or verified by the local implementation:

- Protect `main` with a ruleset: block force pushes/deletion and require the
  workflow's `build` check. Use pull requests and review workflow/Gemfile/template
  changes before publishing. Require another reviewer where collaborators permit.
- Enable Dependabot alerts/security updates, GitHub secret scanning, and push
  protection in [security settings](https://github.com/mobekk/mobekk.github.io/settings/security_analysis).
- Use a passkey/security key for GitHub and the domain registrar; review recovery
  methods, authorized apps, deploy keys, collaborators and PAT scopes.
- Keep domain auto-renewal enabled. Avoid wildcard DNS and remove stale DNS if
  retiring Pages. Keep the domain verification TXT record.
- Renew `.well-known/security.txt` before 2027-10-01, and monitor hello@mobekk.blog.

## Browser policies and hosting limits

The HTML CSP blocks scripts, frames, forms, objects, base-URL changes and network
connections; styles and fonts are local. Only local images and the CSS data-image
texture are allowed. Metadata text/attributes are escaped, and cover images must
match a real static file under `/assets/images/`. Post bodies remain rendered HTML;
put untrusted HTML examples inside fenced code blocks.

A restrictive referrer meta policy and explicit external-link protection are also
present. Google Fonts has been replaced by licensed local font files. Security
checks verify every generated HTML page and reject unexpected public files,
external resource dependencies, executable HTML, missing assets and weakened
policies. Test fixtures exercise HTML/attribute injection, malicious tags/read times,
and invalid remote/traversal image paths. Extend the artifact allowlist deliberately
when adding new page types or assets.

**The remaining headers cannot be configured using native GitHub Pages repository
files.** Do not add an ineffective `_headers` file or pretend that meta tags implement
HSTS, X-Frame-Options or CSP frame-ancestors. If a configurable proxy/host is chosen,
apply these response headers to HTML pages, including error responses:

```text
Content-Security-Policy: default-src 'none'; script-src 'none'; style-src 'self'; font-src 'self'; img-src 'self' data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-src 'none'; frame-ancestors 'none'
Referrer-Policy: no-referrer
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Permissions-Policy: camera=(), microphone=(), geolocation=()
Strict-Transport-Security: max-age=31536000
```

Use `nosniff`, referrer policy, permissions policy and HSTS on asset responses too;
apply CSP at least on HTML. Add HSTS only after confirming HTTPS works for the
chosen host. Do not add `includeSubDomains` or preload until every affected
subdomain has been assessed. Avoid framing JavaScript workarounds: this blog's CSP
intentionally blocks scripts, and client-side frame busting is unreliable.

After deployment, verify:

```sh
curl -I https://mobekk.blog/
curl -I http://mobekk.blog/
curl -I https://mobekk.github.io/
curl -I https://mobekk.blog/.well-known/security.txt
curl -I https://mobekk.blog/Gemfile
curl -I https://mobekk.blog/.git/config
```

Expect HTTPS 200, HTTP-to-HTTPS and github.io-to-custom-domain redirects, a served
security contact file, and 404 for private build/source files. Inspect the rendered
CSP/referrer meta tags separately: they do not appear in HTTP headers. Live hosting
and account changes require authorized service access; local checks do not establish
that those controls are active in production.

## Verification of this change (2026-10-23)

- Frozen production build succeeded on Ruby 3.4.10 with Jekyll 4.4.1.
- Ruby advisory audit passed with the current database and no ignore list.
- All four production HTML pages passed artifact/policy/local-resource checks.
- Ten rendered pages, including six hostile metadata fixtures, passed the same
  checks; invalid image paths were omitted and injection remained escaped text.
- A headless Chromium check loaded the site styles, images and five local font
  files successfully. Existing post URLs and image references were retained.
- Workflow YAML, SHA action pins and deployment permissions were checked locally.
  The GitHub-hosted workflow and production deployment have not been run.

The WEBrick upstream report and hosting/account controls above remain explicit
limitations; a clean advisory scan is not a claim that every possible issue is fixed.
