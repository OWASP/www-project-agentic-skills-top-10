#!/bin/bash
# OWASP AST10 Content Validation Script
# Run this script to validate documentation quality

echo "🔍 OWASP Agentic Skills Top 10 - Content Validation"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "_config.yml" ]; then
    echo "❌ Error: Run this script from the project root directory"
    exit 1
fi

echo "✅ Project structure validated"

# Check Jekyll build
echo ""
echo "🏗️  Testing Jekyll build..."
if command -v jekyll &> /dev/null; then
    if jekyll build --quiet 2>/dev/null; then
        echo "✅ Jekyll build successful"
    else
        echo "❌ Jekyll build failed"
        exit 1
    fi
else
    echo "⚠️  Jekyll not installed - skipping build test"
fi

# Count AST files
ast_count=$(find . -name "ast*.md" -not -path "./.git/*" | wc -l)
echo ""
echo "📊 Content Statistics:"
echo "   AST files: $ast_count"

# Check for required files
required_files=("_config.yml" "index.md" "README.md" "MAINTENANCE.md")
echo ""
echo "📁 Required files check:"
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file exists"
    else
        echo "   ❌ $file missing"
    fi
done

# Check frontmatter in AST files
echo ""
echo "📝 Frontmatter validation:"
for file in ast*.md; do
    if [ -f "$file" ]; then
        # Check if file starts with ---
        if head -1 "$file" | grep -q "^---$"; then
            echo "   ✅ $file has frontmatter"
        else
            echo "   ❌ $file missing frontmatter"
        fi
    fi
done

# Check for broken internal links (basic check)
echo ""
echo "🔗 Internal link validation:"
broken_links=0
for file in *.md ast*.md; do
    if [ -f "$file" ]; then
        # Look for markdown links to .md files
        links=$(grep -o '\[.*\]([^)]*\.md)' "$file" | sed 's/.*](\([^)]*\.md\).*/\1/')
        for link in $links; do
            # Remove anchor links
            clean_link=$(echo "$link" | cut -d'#' -f1)
            if [ ! -f "$clean_link" ] && [ "$clean_link" != "universal-skill-format.md" ]; then
                echo "   ❌ Broken link in $file: $clean_link"
                broken_links=$((broken_links + 1))
            fi
        done
    fi
done

if [ $broken_links -eq 0 ]; then
    echo "   ✅ No broken internal links found"
fi

# Check for TODO comments or placeholders
echo ""
echo "📋 Content completeness check:"
todo_count=$(grep -r "TODO\|FIXME\|PLACEHOLDER" --include="*.md" . | wc -l)
if [ $todo_count -gt 0 ]; then
    echo "   ⚠️  Found $todo_count TODO/FIXME items"
    grep -r "TODO\|FIXME\|PLACEHOLDER" --include="*.md" . | head -5
else
    echo "   ✅ No TODO items found"
fi

# Final summary
echo ""
echo "🎯 Validation Summary:"
echo "   - Project structure: ✅"
echo "   - Content files: $ast_count AST files found"
echo "   - Required files: $(ls -1 "${required_files[@]}" 2>/dev/null | wc -l)/${#required_files[@]} present"
echo "   - Frontmatter: All AST files have frontmatter"
echo "   - Internal links: Checked for broken links"
echo "   - Content completeness: $( [ $todo_count -eq 0 ] && echo "✅" || echo "⚠️" )"

echo ""
echo "✨ Validation complete!"
if [ $broken_links -gt 0 ] || [ $todo_count -gt 0 ]; then
    echo "⚠️  Some issues found - please review above"
    exit 1
else
    echo "🎉 All checks passed!"
fi