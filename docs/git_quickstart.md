# Git 与 GitHub 提交速查

## 1. 获取代码

```bash
git clone <你的仓库地址>
cd wireless-dirvesity-spread-exp
```

## 2. 本地完成实验

```bash
pip install -r requirements.txt
python src/test_environment.py
python src/part1_diversity.py
python src/part2_spread_spectrum.py
python grading/calculate_grade.py
```

## 3. 提交代码

```bash
git status
git add src/ REPORT.md results/
git commit -m "complete experiment 03"
git push
```

## 4. 创建 Pull Request

PR 标题必须包含姓名和学号，推荐格式：

```text
实验03-张三-2024000001
```

提交后查看：

- PR 页面自动评分评论。
- Actions 页面 Summary。
- Actions Artifacts 中的评分报告和结果图。
