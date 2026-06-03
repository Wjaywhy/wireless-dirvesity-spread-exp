# 项目总览：无线通信技术实验 03

本项目是《无线通信技术》课程第三次实验平台，主题为“分集与扩频通信”。

## 实验组织

- Part 1：分集合并
  - 瑞利平坦衰落信道
  - 选择合并 SC
  - 最大比合并 MRC
  - 不同分集阶数 BER 对比
- Part 2：扩频通信
  - m 序列发生器
  - DSSS 扩频与相关解扩
  - 处理增益
  - 窄带干扰下 BER 对比

## 技术栈

- Python
- NumPy
- Matplotlib
- pytest
- GitHub Actions

## 目录说明

```text
src/          学生代码区
grading/      自动评分脚本
docs/         理论文档
materials/    教师 Word/PPT 授课材料
examples/     示例生成脚本
results/      学生实验输出
course_management/ 作业提交跟踪
course_materials/ 课件 PDF 说明
```

## 自动评分

自动评分由 `.github/workflows/grading.yml` 触发，主要检查：

1. Python 环境
2. Part 1 函数正确性与结果图
3. Part 2 函数正确性与结果图
4. 实验报告完整性
5. 代码质量
6. 选做任务

评分结果会写入 PR 评论、Actions Summary 和 Artifacts。
