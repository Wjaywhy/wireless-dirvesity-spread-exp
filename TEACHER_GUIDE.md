# 教师使用说明：分集与扩频通信实验

## 1. 实验定位

本实验对应《无线通信技术》第8章“分集”和第9章“扩展频谱通信”。建议安排 2 学时课堂实验，学生课后补充实验报告。

## 2. 课堂安排建议

### 第一阶段：教师讲解与演示（30~45 分钟）

1. 衰落信道背景：深衰落、链路可靠性和分集思想。
2. SC 与 MRC：分支选择、相位校正、加权合并。
3. 扩频背景：DSSS、PN 序列、相关解扩和处理增益。
4. 窄带干扰演示：扩频前后 BER 对比。
5. GitHub 流程演示：Fork/Clone/PR/自动评分。

### 第二阶段：学生实现（60~75 分钟）

1. 完成 SC 和 MRC 合并函数。
2. 完成分集 BER 仿真并生成曲线。
3. 完成 m 序列、DSSS 扩频、解扩与处理增益。
4. 运行脚本生成结果图。
5. 提交 PR 查看自动评分。

## 3. 发布前检查

```bash
pip install -r requirements.txt
python src/test_environment.py
python -m pytest grading/ -v
python grading/calculate_grade.py
python materials/generate_materials.py
```

还需要创建测试 PR，确认：

- GitHub Actions 成功运行。
- PR 评论正常，或至少 Summary/Artifacts 可见。
- `actions/upload-artifact` 使用 v4。
- README、评分脚本、报告模板中的分值一致。
- PR 标题格式 `实验03-姓名-学号` 已在学生指南、指导书和 PPT 中说明。

## 4. GitHub 仓库设置

建议设置：

- Template repository：开启。
- Actions Workflow permissions：Read and write permissions。
- Allow GitHub Actions to create and approve pull requests：开启。

## 5. 自动评分说明

| 项目 | 分值 |
|---|---:|
| 环境配置 | 5 |
| Part 1 分集合并 | 35 |
| Part 2 DSSS 扩频通信 | 35 |
| 实验报告 | 15 |
| 代码质量 | -10~+5 |
| 选做加分 | +10 |

最终分数封顶 100 分，最低 0 分。

## 6. 已知风险与处理

- 学生只实现单分支等化，未真正合并：查看 Part 1 测试输出和报告解释。
- MRC 忘记使用共轭：高 SNR 下 BER 改善不明显。
- m 序列抽头约定混乱：本实验约定抽头为从左到右的 1-based 位置，输出右端寄存器。
- PR 评论失败：查看 Actions Summary 和 Artifacts。
- 学生代码雷同：结合报告和现场提问人工复核。

## 7. 课件对应关系

- `../08章-分集.pdf`
  - 分集基本思想
  - 选择合并、最大比合并
  - 分集增益与 BER 曲线
- `../09章-扩展频谱通信.pdf`
  - 直接序列扩频
  - PN 序列与相关检测
  - 处理增益与抗干扰
