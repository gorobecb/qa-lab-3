#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class TestWebsite:
  # 1. Check browser configuration in browser_setup_and_teardown
  # 2. Run 'Selenium Tests' configuration
  # 3. Test report will be created in reports/ directory

  @pytest.fixture(autouse=True)
  def browser_setup_and_teardown(self):
    self.use_selenoid = False  # set to True to run tests with Selenoid

    if self.use_selenoid:
      self.browser = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        desired_capabilities = {
          "browserName": "chrome",
          "browserSize": "1920x1080"
        }
      )
    else:
      self.browser = webdriver.Chrome()

    self.browser.maximize_window()
    self.browser.implicitly_wait(10)
    self.browser.get("https://www.youtube.com/")

    yield

    self.browser.close()
    self.browser.quit()


  def test_header(self):
    """this test checks that header is correct"""
    header = self.browser.title

    assert header is not None
    assert header == "YouTube"
    return

  def test_search(self):
    """This test checks that search works right"""
    searchInput = self.browser.find_element(by=By.CSS_SELECTOR, value="input#search")
    searchInput.send_keys("rickroll")
    searchInput.send_keys(Keys.ENTER)

    videoTitles = self.browser.find_elements(by=By.CSS_SELECTOR, value="a#video-title")
    isCorrectVideoFound = False
    for videoTitle in videoTitles:
      if videoTitle.text == "Rick Astley - Never Gonna Give You Up (Official Music Video)":
        isCorrectVideoFound = True
        break

    assert isCorrectVideoFound == True

  def test_link(self):
    """This test checks that search works right"""
    searchInput = self.browser.find_element(by=By.CSS_SELECTOR, value="input#search")
    searchInput.send_keys("rickroll")
    searchInput.send_keys(Keys.ENTER)

    self.browser.find_element(by=By.CSS_SELECTOR, value="a#video-title").click()
    assert self.browser.current_url == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    self.browser.back()
    self.browser.back()
    assert self.browser.current_url == "https://www.youtube.com/"
