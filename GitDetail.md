# Guide to Git for updating and merging branches
```
git checkout main
git fetch upstream
git merge upstream/main    # hoặc git rebase upstream/main

git checkout assignment-report
git rebase main            # cập nhật nhánh làm bài từ nhánh main đã cập nhật
```