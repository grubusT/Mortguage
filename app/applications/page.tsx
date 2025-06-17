"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Search, Plus, Filter, MoreHorizontal, DollarSign, Calendar, User } from "lucide-react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"

interface Application {
  id: number
  clientName: string
  loanAmount: number
  propertyAddress: string
  status: "pre-approval" | "documentation" | "under-review" | "approved" | "rejected"
  progress: number
  submittedDate: string
  expectedCloseDate: string
  loanType: string
}

const mockApplications: Application[] = [
  {
    id: 1,
    clientName: "John Smith",
    loanAmount: 450000,
    propertyAddress: "123 Main St, City, State",
    status: "under-review",
    progress: 75,
    submittedDate: "2024-12-10",
    expectedCloseDate: "2024-12-30",
    loanType: "Conventional",
  },
  {
    id: 2,
    clientName: "Sarah Johnson",
    loanAmount: 320000,
    propertyAddress: "456 Oak Ave, City, State",
    status: "approved",
    progress: 100,
    submittedDate: "2024-12-05",
    expectedCloseDate: "2024-12-25",
    loanType: "FHA",
  },
  {
    id: 3,
    clientName: "Mike Davis",
    loanAmount: 580000,
    propertyAddress: "789 Pine St, City, State",
    status: "documentation",
    progress: 45,
    submittedDate: "2024-12-12",
    expectedCloseDate: "2025-01-15",
    loanType: "Jumbo",
  },
  {
    id: 4,
    clientName: "Emily Brown",
    loanAmount: 275000,
    propertyAddress: "321 Elm St, City, State",
    status: "pre-approval",
    progress: 25,
    submittedDate: "2024-12-15",
    expectedCloseDate: "2025-01-20",
    loanType: "VA",
  },
]

const getStatusColor = (status: string) => {
  switch (status) {
    case "pre-approval":
      return "bg-blue-100 text-blue-800"
    case "documentation":
      return "bg-yellow-100 text-yellow-800"
    case "under-review":
      return "bg-purple-100 text-purple-800"
    case "approved":
      return "bg-green-100 text-green-800"
    case "rejected":
      return "bg-red-100 text-red-800"
    default:
      return "bg-gray-100 text-gray-800"
  }
}

const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount)
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  })
}

export default function ApplicationsPage() {
  const [applications, setApplications] = useState<Application[]>([])
  const [searchTerm, setSearchTerm] = useState("")
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setApplications(mockApplications)
      setLoading(false)
    }, 1000)
  }, [])

  const filteredApplications = applications.filter(
    (app) =>
      app.clientName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      app.propertyAddress.toLowerCase().includes(searchTerm.toLowerCase()),
  )

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
      </div>
    )
  }

  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">Applications</h2>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          New Application
        </Button>
      </div>

      <div className="flex items-center space-x-2">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
          <Input
            placeholder="Search applications..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <Button variant="outline">
          <Filter className="mr-2 h-4 w-4" />
          Filter
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {filteredApplications.map((application) => (
          <Card key={application.id} className="hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-lg">{application.clientName}</CardTitle>
                  <CardDescription>{application.loanType} Loan</CardDescription>
                </div>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="sm">
                      <MoreHorizontal className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem>View Details</DropdownMenuItem>
                    <DropdownMenuItem>Update Status</DropdownMenuItem>
                    <DropdownMenuItem>Add Documents</DropdownMenuItem>
                    <DropdownMenuItem>Contact Client</DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <Badge className={getStatusColor(application.status)}>{application.status.replace("-", " ")}</Badge>
                <span className="text-sm text-muted-foreground">{application.progress}% complete</span>
              </div>

              <Progress value={application.progress} className="h-2" />

              <div className="space-y-2 text-sm">
                <div className="flex items-center space-x-2">
                  <DollarSign className="h-4 w-4 text-muted-foreground" />
                  <span className="font-medium">{formatCurrency(application.loanAmount)}</span>
                </div>
                <div className="flex items-center space-x-2 text-muted-foreground">
                  <User className="h-4 w-4" />
                  <span>{application.propertyAddress}</span>
                </div>
                <div className="flex items-center space-x-2 text-muted-foreground">
                  <Calendar className="h-4 w-4" />
                  <span>Expected close: {formatDate(application.expectedCloseDate)}</span>
                </div>
              </div>

              <div className="pt-2 border-t">
                <p className="text-xs text-muted-foreground">Submitted: {formatDate(application.submittedDate)}</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredApplications.length === 0 && (
        <div className="text-center py-12">
          <p className="text-muted-foreground">No applications found matching your search.</p>
        </div>
      )}
    </div>
  )
}
