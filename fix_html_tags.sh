

HTML_FILES=$(find . -name "*.html")

for file in $HTML_FILES; do
  echo "Processing $file..."
  
  sed -i 's|<li class="mb-2">UniTask<li>|<li class="mb-2">UniTask</li>|g' "$file"
  
  sed -i 's|<li class="mb-2">Стрессоустойчивость\n                              <li>|<li class="mb-2">Стрессоустойчивость</li>|g' "$file"
  
  sed -i 's|<li class="mb-2">Стрессоустойчивость<li>|<li class="mb-2">Стрессоустойчивость</li>|g' "$file"
  
  echo "Completed processing $file"
done

echo "All files have been fixed"
