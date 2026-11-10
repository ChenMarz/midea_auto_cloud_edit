# Contributing

本项目目前只维护美的洗碗机（`T0xE1`）和燃气热水器（`T0xE3`）。提交修改时，请优先保持这两类设备的登录、发现、状态刷新和控制流程稳定。

## 修改设备映射

- 洗碗机映射位于 `custom_components/midea_auto_cloud/device_mapping/T0xE1.py`。
- 燃气热水器映射位于 `custom_components/midea_auto_cloud/device_mapping/T0xE3.py`。
- 通用云端通信逻辑位于 `custom_components/midea_auto_cloud/core/`。

新增实体前，请确认对应的 Home Assistant 平台已经在 `__init__.py` 的 `PLATFORMS` 中启用，并同步检查中英文翻译。

## 提交前检查

1. 使用 Python 编译检查确认没有语法错误。
2. 检查 `git diff`，确认没有误删两个目标设备的映射。
3. 在真实设备上验证状态读取、控制和 Home Assistant 重启后的恢复。

## 许可证

提交代码即表示同意代码按照本项目 [Apache License 2.0](./LICENSE) 发布。
