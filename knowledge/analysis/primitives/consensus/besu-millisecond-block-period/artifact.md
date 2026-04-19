# Besu 毫秒级 Block Period 改造分析

**类型**：primitive-analysis
**状态**：complete
**创建日期**：2026-04-07
**来源**：`openspec/changes/besu-enterprise-millisecond-block-period-support/draft.md`

---

## 概述

Hyperledger Besu 已实现实验性字段 `xblockperiodmilliseconds` 用于支持毫秒级 block period 配置。本分析确认将其提升为生产级特性的可行性和改造成本。

**核心结论**：改造可行，改动量小到中等（约 10-12 个文件），无不可逾越的技术阻塞。

---

## 调用链地图

### 从 Genesis 到运行时的完整路径

```
Genesis JSON (blockperiodseconds / xblockperiodmilliseconds)
    ↓
JsonGenesisConfigOptions.getQbftConfigOptions()
    ↓
JsonBftConfigOptions.getBlockPeriodMilliseconds() / getBlockPeriodSeconds()
    ↓
    ├─→ QbftProtocolScheduleBuilder.createBlockHeaderRuleset()
    │       ↓
    │   Duration.ofMillis(...) / Duration.ofSeconds(...)
    │       ↓
    │   QbftBlockHeaderValidationRulesetFactory.blockHeaderValidator()
    │       ↓
    │   当 duration >= 1s 时添加 TimestampMoreRecentThanParent 规则
    │
    └─→ QbftBesuControllerBuilder.createMiningCoordinator()
            ↓
        new BlockTimer() / new RoundTimer()
            ↓
        BlockTimer.startTimer()
            ↓
        当 milliseconds > 0: expiryTime = clock.millis() + milliseconds
        否则：expiryTime = headerTimestamp * 1000 + seconds * 1000
```

### 关键文件索引

| 层级 | 文件 | 关键方法 |
|------|------|----------|
| Genesis 解析 | `JsonGenesisConfigOptions.java` | `getQbftConfigOptions()` |
| BFT Config | `JsonBftConfigOptions.java` | `getBlockPeriodMilliseconds()` L79-82 |
| Protocol Schedule | `QbftProtocolScheduleBuilder.java` | `createBlockHeaderRuleset()` L133-137 |
| Header Validator | `QbftBlockHeaderValidationRulesetFactory.java` | `blockHeaderValidator()` L81-83 |
| Block Timer | `BlockTimer.java` | `startTimer()` L108-121 |
| Controller Builder | `QbftBesuControllerBuilder.java` | `createMiningCoordinator()` L253-258 |

---

## 限制分析（分层）

| 层次 | 状态 | 说明 |
|------|------|------|
| 配置层 | ✅ 已支持 | `JsonBftConfigOptions` L79-82 已读取毫秒字段 |
| 数据模型层 | ✅ 已支持 | `BftConfigOptions` 返回 `long` 毫秒值 |
| Transition 层 | ✅ 已支持 | `BftFork` L107-109 支持 transition 配置 |
| Protocol Schedule 层 | ✅ 已支持 | 已正确转换为 `Duration` |
| Block Timer 层 | ✅ 已支持 | 毫秒路径使用 `clock.millis()` |
| Header Validator 层 | ✅ 条件绕过 | < 1s 时不添加秒级验证规则 |
| Round Timer 层 | ⚠️ 仅支持秒 | `requesttimeoutseconds` 仅秒级配置 |
| Header Timestamp | ⚠️ 协议级秒级 | Ethereum timestamp 为秒级 |

---

## 必改文件清单

### P0（必须修改）

1. **`config/src/main/java/org/hyperledger/besu/config/JsonBftConfigOptions.java`**
   - L39: 修改 `DEFAULT_BLOCK_PERIOD_MILLISECONDS` 注释
   - L79-82: 移除实验性描述

2. **`config/src/main/java/org/hyperledger/besu/config/BftConfigOptions.java`**
   - L48-52: 更新接口方法注释

3. **`config/src/main/java/org/hyperledger/besu/config/BftFork.java`**
   - L103-109: 更新注释

4. **`config/src/main/java/org/hyperledger/besu/config/MutableBftConfigOptions.java`**
   - L157-165: 更新注释

5. **`consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/BlockTimer.java`**
   - L114-116: 移除或调整 `LOG.warn`

### P1（测试补充）

6. **`config/src/test/java/org/hyperledger/besu/config/JsonBftConfigOptionsTest.java`**
   - 新增毫秒字段解析测试

7. **`consensus/common/src/test/java/org/hyperledger/besu/consensus/common/bft/BlockTimerTest.java`**
   - 新增毫秒级 timer 触发测试

8. **`consensus/qbft/src/test/java/org/hyperledger/besu/consensus/qbft/QbftProtocolScheduleTest.java`**
   - 新增毫秒模式 header validator 规则测试

9. **`consensus/ibft/src/test/java/org/hyperledger/besu/consensus/ibft/IbftProtocolScheduleTest.java`**
   - 同上

10. **`acceptance-tests/tests/src/acceptanceTest/resources/qbft/qbft-millis.json`**
    - 新增测试 genesis

---

## 实现方案

### 推荐方案：方案 A（增量改进）

**策略**：保留 `blockperiodseconds`，将 `xblockperiodmilliseconds` 提升为生产级

**互斥规则**：`xblockperiodmilliseconds > 0` 时优先

**优点**：
- 向后兼容
- 改动面小（5-7 个文件）
- 风险可控

**缺点**：
- 字段带 `x` 前缀
- 双字段并存可能混淆

---

## 关键风险

### 风险 1：Header Timestamp 秒级语义

**问题**：毫秒级出块时，同秒多块的 timestamp 相同

**缓解**：私链场景可控；验证规则已绕过

### 风险 2：Request Timeout 比例失调

**问题**：秒级 timeout 对毫秒出块可能过长

**缓解**：timeout 用于故障检测，1 秒通常足够

### 风险 3：Mining Configuration 监听器

**问题**：监听器只更新秒值

**缓解**：审计使用点，如仅用于指标则影响小

---

## 改动量评估

| 类型 | 文件数 | 行数估算 |
|------|--------|----------|
| 配置层（注释更新） | 4 | ~20 行 |
| 运行时（日志调整） | 1 | ~5 行 |
| 测试层（新增） | 5-7 | ~200-300 行 |
| **合计** | **10-12** | **~225-325 行** |

**改动量**：小到中等

---

## 能力边界

### 协议原生能力

- Block Period 毫秒配置（改造后）
- Block Timer 毫秒级触发
- Header Validator 毫秒模式绕过

### 外部依赖

- Header Timestamp 秒级语义（Ethereum 协议约束）
- Request Timeout 秒级配置（当前限制）

### 非目标

- 不要求与 Ethereum 主网兼容
- 不修改 Header Timestamp 语义
- 不准备上游 PR

---

## 相关对象关系

| 对象 | 关系 | 说明 |
|------|------|------|
| QBFT | 主覆盖 | Besu 的 QBFT 共识实现 |
| IBFT2 | 次覆盖 | 如共用基础设施则适用 |
| BlockTimer | 核心组件 | 出块计时器 |
| RoundTimer | 联动组件 | Round 超时计时器 |
| Header Validator | 验证层 | 区块头验证规则 |

---

## 结论

| 问题 | 结论 |
|------|------|
| **是否可行** | 是 |
| **技术阻塞** | 无不可逾越阻塞 |
| **改动量** | 小到中等（10-12 个文件） |
| **推荐方案** | 方案 A（提升现有实验性字段） |
| **最大风险** | Header Timestamp 秒级语义（可绕过） |

---

## 最小 PoC 路径

**第一步**（配置层）：
- 更新 4 个配置类注释，移除 "Experimental" 描述

**第二步**（运行时）：
- 调整 `BlockTimer.java` 警告日志

**第三步**（测试）：
- 补充 5-7 个测试文件

---

## 参考资料

- 源码路径：`/Users/zhehan/Documents/study/blockchain/besu/code/besu`
- Change Draft：`openspec/changes/besu-enterprise-millisecond-block-period-support/draft.md`
