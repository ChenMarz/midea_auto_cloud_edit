# 美的燃气热水器与洗碗机 Home Assistant 集成

这是一个面向 Home Assistant 的美的云端设备集成，目前只维护两类设备：

- `T0xE1`：洗碗机
- `T0xE3`：燃气热水器

## 安装

将 `custom_components/midea_auto_cloud` 目录复制到 Home Assistant 的 `custom_components` 目录，重启 Home Assistant，然后在“设置 → 设备与服务”中添加集成。

本集成通过美的云端服务工作，并需要安装 `lupa>=2.0`。

## 说明

为了兼容已有的 Home Assistant 配置和设备缓存，本项目暂时保留 `midea_auto_cloud` 作为内部域名。项目只包含洗碗机和燃气热水器的设备映射。

设备对应的 Lua 和插件文件由集成自动下载，并保存在 `.storage/midea_auto_cloud/` 下。

## 许可证

本项目使用 Apache License 2.0 发布。项目是在原有开源项目基础上的维护和修改版本，具体条款请参阅 [LICENSE](./LICENSE)。
