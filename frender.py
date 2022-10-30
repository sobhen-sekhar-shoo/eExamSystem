from math import e
from sre_constants import SUCCESS
from tkinter import Image
from flask import Flask, flash, request,url_for,render_template,redirect,session
from markupsafe import escape
import pymongo
from pymongo import MongoClient
import datetime
import os
from werkzeug.utils import secure_filename

