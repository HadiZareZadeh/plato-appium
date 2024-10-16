import os
import psutil
import re
import subprocess
import threading
import time
import json
import requests
import pandas as pd
from appium import webdriver
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.action_chains import ActionChains
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.common.base import AppiumOptions
from appium import webdriver
from appium.options.android import UiAutomator2Options
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime
import queue
import logging
from PIL import Image
import io

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

ldconsole_path = 'ldconsole.exe'


def find_process_by_port(port):
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port:
            try:
                return psutil.Process(conn.pid).pid
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    return None


def list_ldplayer_instances():
    command = f'"{ldconsole_path}" list2'
    result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    instances = result.stdout.decode().splitlines()
    appium_port = 4723
    system_port = 8200
    adb_port = 5556

    instance_names = []
    for line in instances:
        line = line.split(',')
        instance_names.append({
            "index": line[0],
            "name": line[1],
            "status": line[5] != "-1",
            "appium_port": appium_port,
            "system_port": system_port,
            "adb_port": adb_port,
        })
        appium_port += 1
        system_port += 1
        adb_port += 1
    return instance_names


def stop_appium_server(appium_server_port):
    pid = find_process_by_port(appium_server_port)
    if pid:
        try:
            process = psutil.Process(pid)
            process.terminate()
            process.wait(timeout=5)
            logging.info(
                f"Appium server on port {appium_server_port} has been stopped.")
        except Exception as e:
            logging.error(f"Failed to stop Appium server: {e}")
    else:
        logging.info(f"No process found on port {appium_server_port}")


def main():
    all_instances = list_ldplayer_instances()
    for instance in all_instances:
        instance_appium_port = instance["appium_port"]
        stop_appium_server(instance_appium_port)
    sleep(3)


if __name__ == "__main__":
    main()
