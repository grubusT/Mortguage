import { Calendar, Clock, User } from "lucide-react"
import { Badge } from "@/components/ui/badge"

const reminders = [
  {
    id: 1,
    title: "Follow up with John Smith",
    description: "Check on document submission",
    dueDate: "Today, 2:00 PM",
    priority: "high",
    type: "call",
  },
  {
    id: 2,
    title: "Sarah Johnson consultation",
    description: "Initial mortgage consultation",
    dueDate: "Tomorrow, 10:00 AM",
    priority: "medium",
    type: "meeting",
  },
  {
    id: 3,
    title: "Document deadline",
    description: "Mike Davis - Income verification due",
    dueDate: "Dec 20, 5:00 PM",
    priority: "high",
    type: "document",
  },
  {
    id: 4,
    title: "Lender response expected",
    description: "Emily Brown application review",
    dueDate: "Dec 22, 12:00 PM",
    priority: "low",
    type: "response",
  },
]

const getPriorityColor = (priority: string) => {
  switch (priority) {
    case "high":
      return "bg-red-100 text-red-800"
    case "medium":
      return "bg-yellow-100 text-yellow-800"
    case "low":
      return "bg-green-100 text-green-800"
    default:
      return "bg-gray-100 text-gray-800"
  }
}

const getTypeIcon = (type: string) => {
  switch (type) {
    case "call":
      return <User className="h-4 w-4" />
    case "meeting":
      return <Calendar className="h-4 w-4" />
    case "document":
      return <Clock className="h-4 w-4" />
    default:
      return <Clock className="h-4 w-4" />
  }
}

export function UpcomingReminders() {
  return (
    <div className="space-y-4">
      {reminders.map((reminder) => (
        <div key={reminder.id} className="flex items-start space-x-3 p-3 rounded-lg border">
          <div className="flex-shrink-0 mt-1">{getTypeIcon(reminder.type)}</div>
          <div className="flex-1 space-y-1">
            <div className="flex items-center justify-between">
              <p className="text-sm font-medium">{reminder.title}</p>
              <Badge className={getPriorityColor(reminder.priority)}>{reminder.priority}</Badge>
            </div>
            <p className="text-xs text-muted-foreground">{reminder.description}</p>
            <p className="text-xs text-muted-foreground font-medium">{reminder.dueDate}</p>
          </div>
        </div>
      ))}
    </div>
  )
}
