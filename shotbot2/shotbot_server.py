#!/usr/bin/env python
# coding=utf-8
from flask import Flask, jsonify, request
import shotbot, relay 
import os, json, threading, time, random