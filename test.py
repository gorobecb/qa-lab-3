#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv


class TestWebsite:
  @pytest.fixture(autouse=True)
  def browser_setup_and_teardown(self):
    self.use_selenoid = False

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


  # TASK 1
  def test_header(self):
    """this test checks that header is correct"""
    header = self.browser.title

    assert header is not None
    assert header == "YouTube"
    return

  # TASK 2
  def test_search(self):
    """This test checks that search works right"""
    searchInput = self.browser.find_element(by=By.CSS_SELECTOR, value="input#search")
    searchInput.send_keys("rickroll")
    searchInput.send_keys(Keys.ENTER)

    self.browser.implicitly_wait(10)

    videoTitles = self.browser.find_elements(by=By.CSS_SELECTOR, value="a#video-title")
    isCorrectVideoFound = False
    for videoTitle in videoTitles:
      if videoTitle.text == "Rick Astley - Never Gonna Give You Up (Official Music Video)":
        isCorrectVideoFound = True
        break

    assert isCorrectVideoFound == True

  # TASK 3
  def test_link(self):
    """This test checks that search works right"""
    searchInput = self.browser.find_element(by=By.CSS_SELECTOR, value="input#search")
    searchInput.send_keys("rickroll")
    searchInput.send_keys(Keys.ENTER)
    self.browser.implicitly_wait(10)
    self.browser.find_element(by=By.CSS_SELECTOR, value="a#video-title").click()
    assert self.browser.current_url == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    self.browser.back()
    self.browser.back()
    assert self.browser.current_url == "https://www.youtube.com/"


# Function to load test data
# Could be easily replaced by sql/excel loading, anything
def get_data():
  with open("source/tests.csv") as data_source:
    reader = csv.reader(data_source, delimiter=";")
    next(reader)
    data = [tuple(row) for row in reader]
  return data

class TestWithSources:
  @pytest.fixture(autouse=True)
  def browser_setup_and_teardown(self):
    self.use_selenoid = False

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
    self.browser.get("https://instacalc.com/")

    yield

    self.browser.close()
    self.browser.quit()

  # TASK 5
  @pytest.mark.parametrize("x,operation,y,res", get_data())
  def test_from_source(self, x, operation, y, res):
    inputEl = self.browser.find_element(by=By.CSS_SELECTOR, value="calc rows c1 input")
    inputEl.send_keys(f"{x} {operation} {y}")

    outputEl = self.browser.find_element(by=By.CSS_SELECTOR, value="calc rows c2 div")

    assert outputEl.text == res