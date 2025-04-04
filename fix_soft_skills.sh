

HTML_FILES=$(find . -name "*.html")

for file in $HTML_FILES; do
  echo "Processing $file..."
  
  sed -i 's|<li class="mb-2">Стрессоустойчивость\n                              <li>|<li class="mb-2">Стрессоустойчивость</li>|g' "$file"
  
  perl -i -0pe 's|<li class="mb-2">Стрессоустойчивость\s*<li>|<li class="mb-2">Стрессоустойчивость</li>|gs' "$file"
  
  echo "Completed processing $file"
done

echo "All files have been fixed"
