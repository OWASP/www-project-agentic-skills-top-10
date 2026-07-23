#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
fixture_dir=$(mktemp -d)

cleanup() {
    rm -rf "$fixture_dir"
}
trap cleanup EXIT

mkdir -p "$fixture_dir/bin"
cp "$repo_root/validate.sh" "$fixture_dir/validate.sh"

printf '%s\n' "title: Validation fixture" > "$fixture_dir/_config.yml"
for file in index.md README.md MAINTENANCE.md universal-skill-format.md; do
    printf '# Validation fixture\n' > "$fixture_dir/$file"
done
printf '%s\n' "---" "title: Valid AST fixture" "---" > "$fixture_dir/ast01.md"

# Keep the regression test independent of whether Jekyll is installed locally.
printf '%s\n' '#!/usr/bin/env bash' 'exit 0' > "$fixture_dir/bin/jekyll"
chmod +x "$fixture_dir/bin/jekyll"

(
    cd "$fixture_dir"
    PATH="$fixture_dir/bin:$PATH" bash ./validate.sh > clean.log
)
grep -q "All checks passed" "$fixture_dir/clean.log"

printf '# Invalid AST fixture\n' > "$fixture_dir/ast99.md"

if (
    cd "$fixture_dir"
    PATH="$fixture_dir/bin:$PATH" bash ./validate.sh > invalid.log
); then
    echo "Expected validation to fail for missing AST frontmatter" >&2
    exit 1
fi

grep -q "ast99.md missing frontmatter" "$fixture_dir/invalid.log"
grep -q "1 AST file(s) missing frontmatter" "$fixture_dir/invalid.log"

echo "Validator frontmatter regression tests passed"
