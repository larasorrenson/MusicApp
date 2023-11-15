from flask import Blueprint, render_template, flash, request ,redirect, url_for
from .models import Booking, Concert
from datetime import datetime
#from .forms import BookingForm, UpdateBookingForm
from . import db
import sqlalchemy
from sqlalchemy.sql import text, func
import os


def showEventStatus(id):
    current_dateTime = datetime.now()
    date = db.session.scalar(db.select(Concert.EventDate).where(Concert.id==id))
    time = db.session.scalar(db.select(Concert.EventTime).where(Concert.id==id))
    dateTime_string = date + " " + time + ":00"
    eventDateTime = datetime.strptime(dateTime_string, '%d/%m/%Y %H:%M:%S')

    TotalQuery = sqlalchemy.select(sqlalchemy.func.sum(Booking.TicketQuantity)).where(Booking.EventID==id)
    EventQuery = sqlalchemy.select(Concert.EventTicketCount).where(Concert.id==id)

    TotalTickets = db.session.execute(TotalQuery).scalar()
    EventTickets = db.session.execute(EventQuery).scalar()

    if TotalTickets == None:
        TotalTickets = 0

    print(TotalTickets)
    print(EventTickets)

    statusQuery = sqlalchemy.select(Concert.EventStatus).where(Concert.id==id)
    EventStatus = db.session.execute(statusQuery).scalar()

    print(EventStatus)
    if (eventDateTime <= current_dateTime):
        EventStatus = "Inactive"
    elif (TotalTickets >= EventTickets):
        EventStatus = "Sold Out"
    elif (EventStatus == "Cancelled"):
        EventStatus = "Cancelled"
    else:
        EventStatus = "Open"


    return(EventStatus)
    




