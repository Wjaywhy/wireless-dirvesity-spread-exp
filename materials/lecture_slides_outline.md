# 无线通信技术实验 03 课堂讲解 PPT 大纲

## Slide 01：封面
- 无线通信技术实验 03
- 分集与扩频通信
- SC/MRC 分集合并 + DSSS 扩频通信
- 代码补全、仿真验证、GitHub 自动评分

## Slide 02：本次实验要解决的问题
- 衰落会让接收信号突然变弱
- 分集用多个独立副本降低深衰落概率
- 扩频用 PN 码把信号能量铺展到更宽带宽
- 解扩相关可以恢复目标信号并摊薄干扰

## Slide 03：课堂流程
- 0-10 分钟：实验背景和目标
- 10-35 分钟：SC、MRC、DSSS 原理
- 35-50 分钟：仓库结构与自动评分演示
- 50-110 分钟：学生完成 TODO 并生成结果图
- 110-120 分钟：提交 PR，查看评分反馈

## Slide 04：Part 1 分集模型
- BPSK 符号经过多个独立瑞利衰落分支
- 每个分支都有自己的信道系数和噪声
- 接收端需要把多个分支合成一个判决变量
- 观察 BER 随 SNR 和合并方法变化

## Slide 05：选择合并 SC
- 每个符号选择瞬时信道最强的分支
- 指标是 |h|^2
- 输出为被选分支的 r/h
- 优点是简单，缺点是没有利用所有分支

## Slide 06：最大比合并 MRC
- 每个分支乘以信道共轭做相位校正
- 信道强的分支获得更大权重
- 归一化项是所有分支 |h|^2 之和
- MRC 通常获得最佳合并 SNR

## Slide 07：Part 1 代码入口
- 文件：src/part1_diversity.py
- 完成 selection_combining
- 完成 maximal_ratio_combining
- 完成 simulate_diversity_ber
- 运行后生成 diversity_ber_curve.png 和 diversity_waveform_snapshot.png

## Slide 08：Part 2 DSSS 链路
- 比特先映射为 BPSK 符号
- 每个符号乘以一段 PN 码片序列
- 信道中加入噪声和窄带干扰
- 接收端用同一 PN 序列相关解扩

## Slide 09：m 序列约定
- 寄存器从左到右书写
- 抽头为从左到右的 1-based 位置
- 每拍输出右端寄存器
- 抽头异或得到反馈并插入左端
- 输出比特映射为 0->+1，1->-1

## Slide 10：扩频、解扩和处理增益
- 扩频输出长度等于比特数乘扩频因子
- 解扩是每个符号周期内的相关累加
- 非负相关判 bit 0，负相关判 bit 1
- 处理增益为 10log10(N) dB

## Slide 11：Part 2 代码入口
- 文件：src/part2_spread_spectrum.py
- 完成 generate_m_sequence
- 完成 dsss_spread 和 dsss_despread
- 完成 processing_gain_db
- 运行后生成 dsss_ber_curve.png 和 dsss_correlation_snapshot.png

## Slide 12：本地运行流程
- pip install -r requirements.txt
- python src/test_environment.py
- python src/part1_diversity.py
- python src/part2_spread_spectrum.py
- python grading/calculate_grade.py

## Slide 13：GitHub 提交流程
- 完成代码和 REPORT.md
- 提交 results/ 中的四张结果图
- Commit & Push 到自己的仓库
- 向教师仓库创建 Pull Request
- PR 标题格式：实验03-姓名-学号

## Slide 14：自动评分与作业跟踪
- PR 评论显示总分和测试摘要
- Actions Summary 保留完整评分输出
- Artifacts 上传评分报告和结果图
- 作业跟踪表区分未提交、未评分和已评分

## Slide 15：评分标准
- 环境配置 5 分
- Part 1 分集合并 35 分
- Part 2 DSSS 扩频通信 35 分
- 实验报告 15 分
- 代码质量 -10 到 +5 分
- 选做加分最多 10 分

## Slide 16：常见问题
- MRC 漏掉共轭会导致复信道下结果异常
- m 序列全零初始状态无效
- 解扩输入长度必须是 PN 长度整数倍
- 结果图缺失会影响自动评分
- PR 标题缺少姓名学号会影响作业跟踪

## Slide 17：AI 使用边界
- 可以请 AI 解释公式和报错
- 可以请 AI 协助检查报告结构
- 必须能解释自己提交的核心函数
- 报告中说明 AI 辅助内容和验证方式

## Slide 18：课堂收束
- 分集解决衰落可靠性问题
- MRC 通过相位校正和幅度加权提升 SNR
- DSSS 通过扩频和相关解扩获得处理增益
- 自动评分帮助快速定位实现问题
