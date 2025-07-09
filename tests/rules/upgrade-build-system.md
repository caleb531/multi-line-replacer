## setuptools build-system

```toml
[build-system]
requires = ["MATCH_ENV_PROJECT_BUILD_SYSTEM"]
build-backend = "MATCH_ENV_PROJECT_BUILD_BACKEND"
```

# uv_build build-system

```toml
[build-system]
requires = ["uv_build>=0.7.19,<0.8.0"]
build-backend = "uv_build"

[tool.uv.build-backend]
module-name = "MATCH_ENV_PROJECT_PKG_NAME"
module-root = ""
```
