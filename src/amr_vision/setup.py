from setuptools import find_packages, setup

package_name = "amr_vision"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (
            "share/" + package_name + "/launch",
            [
                "launch/vision.launch.py",
                "launch/canny.launch.py",
                "launch/perception.launch.py",
            ],
        ),
        ("share/" + package_name + "/config", ["config/vision.yaml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="AMR Project",
    maintainer_email="maintainer@example.com",
    description=(
        "OpenCV-based image processing for the AMR platform "
        "(Sprint 7 Phase 2: grayscale conversion)."
    ),
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "gray_converter = amr_vision.gray_converter:main",
            "canny_detector = amr_vision.canny_detector:main",
        ],
    },
)
