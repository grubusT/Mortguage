import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Users, ClipboardList, Clock, CheckCircle } from "lucide-react"

interface DashboardStatsProps {
  stats: {
    totalClients: number
    activeApplications: number
    pendingTasks: number
    completedThisMonth: number
  }
}

export function DashboardStats({ stats }: DashboardStatsProps) {
  const statCards = [
    {
      title: "Total Clients",
      value: stats.totalClients,
      icon: Users,
      description: "+12% from last month",
      color: "text-blue-600",
    },
    {
      title: "Active Applications",
      value: stats.activeApplications,
      icon: ClipboardList,
      description: "+5 new this week",
      color: "text-green-600",
    },
    {
      title: "Pending Tasks",
      value: stats.pendingTasks,
      icon: Clock,
      description: "3 due today",
      color: "text-orange-600",
    },
    {
      title: "Completed This Month",
      value: stats.completedThisMonth,
      icon: CheckCircle,
      description: "+23% from last month",
      color: "text-purple-600",
    },
  ]

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {statCards.map((stat, index) => (
        <Card key={index}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
            <stat.icon className={`h-4 w-4 ${stat.color}`} />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stat.value}</div>
            <p className="text-xs text-muted-foreground">{stat.description}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
