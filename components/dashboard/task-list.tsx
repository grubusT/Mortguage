import { Checkbox } from "@/components/ui/checkbox"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { MoreHorizontal } from "lucide-react"

const tasks = [
  {
    id: 1,
    title: "Review John Smith's credit report",
    description: "Analyze credit score and payment history",
    priority: "high",
    dueDate: "Today",
    completed: false,
    client: "John Smith",
  },
  {
    id: 2,
    title: "Prepare loan comparison for Sarah Johnson",
    description: "Compare rates from 3 different lenders",
    priority: "medium",
    dueDate: "Tomorrow",
    completed: false,
    client: "Sarah Johnson",
  },
  {
    id: 3,
    title: "Schedule property appraisal",
    description: "Coordinate with appraiser for Mike Davis property",
    priority: "high",
    dueDate: "Dec 20",
    completed: false,
    client: "Mike Davis",
  },
  {
    id: 4,
    title: "Update client portal",
    description: "Upload pre-approval letter for Emily Brown",
    priority: "low",
    dueDate: "Dec 22",
    completed: true,
    client: "Emily Brown",
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

export function TaskList() {
  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <div
          key={task.id}
          className={`flex items-start space-x-3 p-3 rounded-lg border ${task.completed ? "opacity-60" : ""}`}
        >
          <Checkbox checked={task.completed} className="mt-1" />
          <div className="flex-1 space-y-1">
            <div className="flex items-center justify-between">
              <p className={`text-sm font-medium ${task.completed ? "line-through" : ""}`}>{task.title}</p>
              <div className="flex items-center space-x-2">
                <Badge className={getPriorityColor(task.priority)}>{task.priority}</Badge>
                <Button variant="ghost" size="sm">
                  <MoreHorizontal className="h-4 w-4" />
                </Button>
              </div>
            </div>
            <p className="text-xs text-muted-foreground">{task.description}</p>
            <div className="flex items-center justify-between">
              <p className="text-xs text-muted-foreground">Client: {task.client}</p>
              <p className="text-xs text-muted-foreground font-medium">Due: {task.dueDate}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
