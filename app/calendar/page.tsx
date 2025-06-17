"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ChevronLeft, ChevronRight, Plus, CalendarIcon, Clock, User } from "lucide-react"

interface Event {
  id: number
  title: string
  client: string
  time: string
  type: "consultation" | "follow-up" | "closing" | "document-review"
  date: string
}

const mockEvents: Event[] = [
  {
    id: 1,
    title: "Initial Consultation",
    client: "John Smith",
    time: "10:00 AM",
    type: "consultation",
    date: "2024-12-17",
  },
  {
    id: 2,
    title: "Document Review",
    client: "Sarah Johnson",
    time: "2:00 PM",
    type: "document-review",
    date: "2024-12-17",
  },
  {
    id: 3,
    title: "Follow-up Call",
    client: "Mike Davis",
    time: "11:00 AM",
    type: "follow-up",
    date: "2024-12-18",
  },
  {
    id: 4,
    title: "Closing Meeting",
    client: "Emily Brown",
    time: "3:00 PM",
    type: "closing",
    date: "2024-12-19",
  },
]

const getEventTypeColor = (type: string) => {
  switch (type) {
    case "consultation":
      return "bg-blue-100 text-blue-800"
    case "follow-up":
      return "bg-yellow-100 text-yellow-800"
    case "closing":
      return "bg-green-100 text-green-800"
    case "document-review":
      return "bg-purple-100 text-purple-800"
    default:
      return "bg-gray-100 text-gray-800"
  }
}

const daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
const months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
]

export default function CalendarPage() {
  const [currentDate, setCurrentDate] = useState(new Date())
  const [selectedDate, setSelectedDate] = useState(new Date())

  const getDaysInMonth = (date: Date) => {
    return new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate()
  }

  const getFirstDayOfMonth = (date: Date) => {
    return new Date(date.getFullYear(), date.getMonth(), 1).getDay()
  }

  const navigateMonth = (direction: "prev" | "next") => {
    setCurrentDate((prev) => {
      const newDate = new Date(prev)
      if (direction === "prev") {
        newDate.setMonth(prev.getMonth() - 1)
      } else {
        newDate.setMonth(prev.getMonth() + 1)
      }
      return newDate
    })
  }

  const getEventsForDate = (date: Date) => {
    const dateString = date.toISOString().split("T")[0]
    return mockEvents.filter((event) => event.date === dateString)
  }

  const renderCalendarDays = () => {
    const daysInMonth = getDaysInMonth(currentDate)
    const firstDay = getFirstDayOfMonth(currentDate)
    const days = []

    // Empty cells for days before the first day of the month
    for (let i = 0; i < firstDay; i++) {
      days.push(<div key={`empty-${i}`} className="h-24 border border-gray-200"></div>)
    }

    // Days of the month
    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(currentDate.getFullYear(), currentDate.getMonth(), day)
      const events = getEventsForDate(date)
      const isToday = date.toDateString() === new Date().toDateString()
      const isSelected = date.toDateString() === selectedDate.toDateString()

      days.push(
        <div
          key={day}
          className={`h-24 border border-gray-200 p-1 cursor-pointer hover:bg-gray-50 ${
            isToday ? "bg-blue-50" : ""
          } ${isSelected ? "ring-2 ring-blue-500" : ""}`}
          onClick={() => setSelectedDate(date)}
        >
          <div className={`text-sm font-medium ${isToday ? "text-blue-600" : ""}`}>{day}</div>
          <div className="space-y-1 mt-1">
            {events.slice(0, 2).map((event) => (
              <div key={event.id} className="text-xs p-1 rounded bg-blue-100 text-blue-800 truncate">
                {event.time} - {event.client}
              </div>
            ))}
            {events.length > 2 && <div className="text-xs text-gray-500">+{events.length - 2} more</div>}
          </div>
        </div>,
      )
    }

    return days
  }

  const selectedDateEvents = getEventsForDate(selectedDate)

  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">Calendar</h2>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          New Event
        </Button>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Calendar */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-xl">
                  {months[currentDate.getMonth()]} {currentDate.getFullYear()}
                </CardTitle>
                <div className="flex space-x-2">
                  <Button variant="outline" size="sm" onClick={() => navigateMonth("prev")}>
                    <ChevronLeft className="h-4 w-4" />
                  </Button>
                  <Button variant="outline" size="sm" onClick={() => navigateMonth("next")}>
                    <ChevronRight className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-7 gap-0">
                {daysOfWeek.map((day) => (
                  <div
                    key={day}
                    className="h-10 flex items-center justify-center font-medium text-sm text-gray-500 border-b"
                  >
                    {day}
                  </div>
                ))}
                {renderCalendarDays()}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Events for selected date */}
        <div>
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <CalendarIcon className="h-5 w-5" />
                <span>
                  {selectedDate.toLocaleDateString("en-US", {
                    weekday: "long",
                    month: "long",
                    day: "numeric",
                  })}
                </span>
              </CardTitle>
              <CardDescription>
                {selectedDateEvents.length} event{selectedDateEvents.length !== 1 ? "s" : ""} scheduled
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {selectedDateEvents.length === 0 ? (
                <p className="text-sm text-muted-foreground">No events scheduled for this date.</p>
              ) : (
                selectedDateEvents.map((event) => (
                  <div key={event.id} className="p-3 border rounded-lg space-y-2">
                    <div className="flex items-center justify-between">
                      <h4 className="font-medium">{event.title}</h4>
                      <Badge className={getEventTypeColor(event.type)}>{event.type.replace("-", " ")}</Badge>
                    </div>
                    <div className="space-y-1 text-sm text-muted-foreground">
                      <div className="flex items-center space-x-2">
                        <Clock className="h-4 w-4" />
                        <span>{event.time}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <User className="h-4 w-4" />
                        <span>{event.client}</span>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </CardContent>
          </Card>

          {/* Upcoming Events */}
          <Card className="mt-6">
            <CardHeader>
              <CardTitle>Upcoming Events</CardTitle>
              <CardDescription>Next 7 days</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {mockEvents.slice(0, 4).map((event) => (
                <div key={event.id} className="flex items-center space-x-3 p-2 rounded-lg border">
                  <div className="text-center">
                    <div className="text-sm font-medium">{new Date(event.date).getDate()}</div>
                    <div className="text-xs text-muted-foreground">
                      {new Date(event.date).toLocaleDateString("en-US", { month: "short" })}
                    </div>
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium">{event.title}</p>
                    <p className="text-xs text-muted-foreground">
                      {event.client} • {event.time}
                    </p>
                  </div>
                  <Badge className={getEventTypeColor(event.type)}>{event.type.replace("-", " ")}</Badge>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
