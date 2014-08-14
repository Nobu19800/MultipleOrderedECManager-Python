#!/usr/bin/env python
# -*- Python -*-

import sys,os

import OpenRTM_aist

def main():
  manager = OpenRTM_aist.Manager.init(sys.argv)

  manager.activateManager()

  manager.runManager()

  return

if __name__ == "__main__":
  main()
