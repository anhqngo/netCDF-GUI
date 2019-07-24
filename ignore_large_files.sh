# Run this scripts to add large files (>50 Mb) to .gitignore

find . -size +50M | cat >> .gitignore