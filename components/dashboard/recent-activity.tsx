import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"

const activities = [
  {
    id: 1,
    client: "John Smith",
    action: "Uploaded income verification",
    time: "2 hours ago",
    status: "completed",
    avatar: "JS",
  },
  {
    id: 2,
    client: "Sarah Johnson",
    action: "Application approved by lender",
    time: "4 hours ago",
    status: "approved",
    avatar: "SJ",
  },
  {
    id: 3,
    client: "Mike Davis",
    action: "Requested additional documents",
    time: "6 hours ago",
    status: "pending",
    avatar: "MD",
  },
  {
    id: 4,
    client: "Emily Brown",
    action: "Initial consultation scheduled",
    time: "1 day ago",
    status: "scheduled",
    avatar: "EB",
  },
  {
    id: 5,
    client: "David Wilson",
    action: "Pre-approval completed",
    time: "2 days ago",
    status: "completed",
    avatar: "DW",
  },
]

const getStatusColor = (status: string) => {
  switch (status) {
    case "completed":
      return "bg-green-100 text-green-800"
    case "approved":
      return "bg-blue-100 text-blue-800"
    case "pending":
      return "bg-yellow-100 text-yellow-800"
    case "scheduled":
      return "bg-purple-100 text-purple-800"
    default:
      return "bg-gray-100 text-gray-800"
  }
}

export function RecentActivity() {
  return (
    <div className="space-y-4">
      {activities.map((activity) => (
        <div key={activity.id} className="flex items-center space-x-4">
          <Avatar className="h-9 w-9">
            <AvatarImage src={`/placeholder.svg?height=36&width=36`} />
            <AvatarFallback>{activity.avatar}</AvatarFallback>
          </Avatar>
          <div className="flex-1 space-y-1">
            <p className="text-sm font-medium leading-none">{activity.client}</p>
            <p className="text-sm text-muted-foreground">{activity.action}</p>
          </div>
          <div className="flex flex-col items-end space-y-1">
            <Badge className={getStatusColor(activity.status)}>{activity.status}</Badge>
            <p className="text-xs text-muted-foreground">{activity.time}</p>
          </div>
        </div>
      ))}
    </div>
  )
}
