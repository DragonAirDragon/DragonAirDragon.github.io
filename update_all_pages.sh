

HTML_FILES=$(find . -name "*.html" -not -name "index.html")

for file in $HTML_FILES; do
  echo "Processing $file..."
  
  sed -i 's|<link id="additional-style" rel="stylesheet" href="assets/css/resume.css">|<link id="additional-style" rel="stylesheet" href="assets/css/resume.css">\n   <link rel="stylesheet" href="assets/css/dark-mode.css">|' "$file"
  
  sed -i 's|<body>|<body>\n   <!-- Dark Mode Toggle -->\n   <div class="dark-mode-toggle">\n      <span class="light-icon"><i class="fas fa-sun"></i></span>\n      <label class="switch">\n         <input type="checkbox" id="darkModeToggle">\n         <span class="slider"></span>\n      </label>\n      <span class="dark-icon"><i class="fas fa-moon"></i></span>\n   </div>\n   |' "$file"
  
  sed -i 's|<script src="assets/js/bootstrap.min.js"></script>|<script src="assets/js/bootstrap.min.js"></script>\n   <script src="assets/js/dark-mode.js"></script>|' "$file"
  
  sed -i 's|<li class="mb-2">UniTask<li>|<li class="mb-2">UniTask</li>|' "$file"
  sed -i 's|<li class="mb-2">Стрессоустойчивость\n                              <li>|<li class="mb-2">Стрессоустойчивость</li>|' "$file"
  
  echo "Completed processing $file"
done

echo "All files have been updated with dark mode functionality"
