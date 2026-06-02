import pkgutil
import sys


def _all_fennflow_modules() -> set[str]:
    import fennflow as pkg

    return {
        m.name for m in pkgutil.walk_packages(pkg.__path__, prefix=pkg.__name__ + ".")
    }


def test_import_all_modules():
    already_imported = set(sys.modules)
    remaining = _all_fennflow_modules() - already_imported

    failed = {}
    for module_name in remaining:
        try:
            __import__(module_name)
        except Exception as e:  # noqa: BLE001
            failed[module_name] = e

    assert not failed, "\n".join(f"{m}: {e}" for m, e in failed.items())
