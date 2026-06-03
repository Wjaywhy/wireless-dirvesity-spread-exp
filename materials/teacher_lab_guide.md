# 无线通信技术实验 03：分集与扩频通信实验指导手册

## 1. 实验前准备

本实验对应第8章“分集”和第9章“扩展频谱通信”。学生需要提前完成：安装 Python 3.9 或更高版本、注册 GitHub 账号、阅读 `README.md` 和 `docs/` 理论文档。

## 2. 课堂时间安排

| 阶段 | 时间 | 内容 |
| --- | ---: | --- |
| 导入 | 10 分钟 | 衰落、深衰落、分集和扩频应用场景 |
| 理论讲解 | 25 分钟 | SC/MRC 公式，DSSS 扩频与相关解扩 |
| 代码演示 | 15 分钟 | 仓库结构、环境测试、自动评分流程 |
| 学生实现 | 60 分钟 | 完成 Part 1 和 Part 2 TODO |
| 提交检查 | 10 分钟 | 生成结果图、提交 PR、查看评分 |

## 3. 仓库结构

```text
src/          学生代码区
grading/      自动评分脚本
docs/         理论文档
materials/    教师授课材料
examples/     示例运行入口
results/      学生输出图像
course_management/ 作业跟踪表
```

## 4. 环境配置

```bash
pip install -r requirements.txt
python src/test_environment.py
```

看到 `环境配置正确` 即可进入实验。

## 5. 学生需要补全的函数

### 5.1 selection_combining(received, channel)

- 输入：`received` 和 `channel`，形状均为 `(num_branches, num_symbols)`。
- 输出：一维复数数组，表示每个符号的均衡估计。
- 提示：每个符号选择 `|h|^2` 最大的分支，然后做 `r / h`。
- 评分点：能正确选择分支、输出长度正确、无噪声时恢复符号。

### 5.2 maximal_ratio_combining(received, channel)

- 输入：多分支接收信号和信道估计。
- 输出：MRC 合并后的符号估计。
- 提示：实现 `sum(conj(h) * r) / sum(|h|^2)`。
- 评分点：使用共轭、正确归一化、无噪声时恢复符号。

### 5.3 simulate_diversity_ber(snr_db_values, num_bits, num_branches, seed)

- 输入：SNR 列表、比特数、分支数和随机种子。
- 输出：包含 `单分支`、`SC`、`MRC` 三条 BER 曲线的字典。
- 提示：使用 `utils.rayleigh_fading_branches` 生成多分支接收信号。
- 评分点：返回格式正确，BER 在 `[0, 1]`，高 SNR 下 MRC 不差于单分支。

### 5.4 generate_m_sequence(register_state, taps, length=None)

- 输入：二进制寄存器初始状态、抽头位置、输出长度。
- 输出：双极性 PN 码片，取值为 `+1` 或 `-1`。
- 提示：输出右端寄存器，反馈插入左端，抽头为从左到右的 1-based 位置。
- 评分点：周期长度、取值集合、参考序列一致。

### 5.5 dsss_spread(bits, pn_chips)

- 输入：0/1 比特和双极性 PN 码片。
- 输出：扩频后的码片序列。
- 提示：先 BPSK 映射，再用每个符号乘完整 PN 序列。
- 评分点：输出长度为 `len(bits) * len(pn_chips)`，码片符号正确。

### 5.6 dsss_despread(received_chips, pn_chips)

- 输入：接收码片和同一 PN 码片序列。
- 输出：判决后的 0/1 比特。
- 提示：按扩频因子 reshape，逐行与 PN 做相关。
- 评分点：小噪声下能恢复比特，输入长度检查正确。

### 5.7 processing_gain_db(spreading_factor)

- 输入：扩频因子 `N`。
- 输出：处理增益 `10 log10(N)`，单位 dB。
- 评分点：公式正确，非法输入抛出异常。

## 6. 本地测试命令

```bash
python src/part1_diversity.py
python src/part2_spread_spectrum.py
python -m pytest grading/test_part1_diversity.py -v
python -m pytest grading/test_part2_spread_spectrum.py -v
python grading/calculate_grade.py
```

## 7. 结果图要求

`results/` 至少应包含：

- `diversity_ber_curve.png`
- `diversity_waveform_snapshot.png`
- `dsss_ber_curve.png`
- `dsss_correlation_snapshot.png`

## 8. 报告要求

报告文件命名为 `REPORT.md`，建议从 `REPORT_TEMPLATE.md` 复制后填写。报告需要包含实验目的、实验原理、实验方法、实验结果、结果分析、实验心得和参考资料。

## 9. GitHub PR 要求

PR 标题必须包含姓名和学号，推荐格式：

```text
实验03-姓名-学号
```

## 10. 自动评分查看方式

提交 PR 后查看 PR 评论、Actions Summary、Artifacts 和教师发布的作业实时跟踪表。

## 11. 评分标准

| 项目 | 分值 |
| --- | ---: |
| 环境配置 | 5 |
| Part 1：分集合并 | 35 |
| Part 2：DSSS 扩频通信 | 35 |
| 实验报告 | 15 |
| 代码质量 | -10~+5 |
| 选做加分 | +10 |

## 12. AI 助手使用边界

可以使用 AI 辅助解释公式、定位报错和检查报告，但必须理解并能解释自己提交的核心函数。报告中必须说明 AI 使用情况。

## 13. FAQ

### MRC 为什么要用共轭？

复信道会改变相位，乘以 `conj(h)` 可以做相位校正，并按信道幅度加权。

### m 序列为什么不能全零初始状态？

全零状态反馈后仍然是全零，无法产生伪随机序列。

### DSSS 为什么能抗窄带干扰？

解扩相关会把同步的目标信号重新集中，同时把未同步干扰扩展摊薄。

## 14. 命令速查

```bash
pip install -r requirements.txt
python src/test_environment.py
python src/part1_diversity.py
python src/part2_spread_spectrum.py
python grading/calculate_grade.py
git add src/ REPORT.md results/
git commit -m "complete experiment 03"
git push
```
