"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Search, Filter, MoreHorizontal, FileText, Download, Eye, Upload } from "lucide-react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"

interface Document {
  id: number
  name: string
  type: string
  clientName: string
  uploadDate: string
  size: string
  status: "pending" | "approved" | "rejected" | "under-review"
}

const mockDocuments: Document[] = [
  {
    id: 1,
    name: "Income_Verification_John_Smith.pdf",
    type: "Income Verification",
    clientName: "John Smith",
    uploadDate: "2024-12-15",
    size: "2.4 MB",
    status: "approved",
  },
  {
    id: 2,
    name: "Credit_Report_Sarah_Johnson.pdf",
    type: "Credit Report",
    clientName: "Sarah Johnson",
    uploadDate: "2024-12-14",
    size: "1.8 MB",
    status: "under-review",
  },
  {
    id: 3,
    name: "Bank_Statements_Mike_Davis.pdf",
    type: "Bank Statements",
    clientName: "Mike Davis",
    uploadDate: "2024-12-13",
    size: "3.2 MB",
    status: "pending",
  },
  {
    id: 4,
    name: "Property_Appraisal_Emily_Brown.pdf",
    type: "Property Appraisal",
    clientName: "Emily Brown",
    uploadDate: "2024-12-12",
    size: "5.1 MB",
    status: "approved",
  },
]

const getStatusColor = (status: string) => {
  switch (status) {
    case "approved":
      return "bg-green-100 text-green-800"
    case "under-review":
      return "bg-yellow-100 text-yellow-800"
    case "pending":
      return "bg-blue-100 text-blue-800"
    case "rejected":
      return "bg-red-100 text-red-800"
    default:
      return "bg-gray-100 text-gray-800"
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  })
}

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([])
  const [searchTerm, setSearchTerm] = useState("")
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setDocuments(mockDocuments)
      setLoading(false)
    }, 1000)
  }, [])

  const filteredDocuments = documents.filter(
    (doc) =>
      doc.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      doc.clientName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      doc.type.toLowerCase().includes(searchTerm.toLowerCase()),
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
        <h2 className="text-3xl font-bold tracking-tight">Documents</h2>
        <Button>
          <Upload className="mr-2 h-4 w-4" />
          Upload Document
        </Button>
      </div>

      <div className="flex items-center space-x-2">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
          <Input
            placeholder="Search documents..."
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
        {filteredDocuments.map((document) => (
          <Card key={document.id} className="hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3">
                  <FileText className="h-8 w-8 text-blue-600 mt-1" />
                  <div className="flex-1">
                    <CardTitle className="text-sm font-medium leading-tight">{document.name}</CardTitle>
                    <CardDescription className="mt-1">{document.type}</CardDescription>
                  </div>
                </div>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="sm">
                      <MoreHorizontal className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem>
                      <Eye className="mr-2 h-4 w-4" />
                      View
                    </DropdownMenuItem>
                    <DropdownMenuItem>
                      <Download className="mr-2 h-4 w-4" />
                      Download
                    </DropdownMenuItem>
                    <DropdownMenuItem>Edit</DropdownMenuItem>
                    <DropdownMenuItem className="text-red-600">Delete</DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <Badge className={getStatusColor(document.status)}>{document.status.replace("-", " ")}</Badge>

              <div className="space-y-1 text-sm text-muted-foreground">
                <p>Client: {document.clientName}</p>
                <p>Size: {document.size}</p>
                <p>Uploaded: {formatDate(document.uploadDate)}</p>
              </div>

              <div className="flex space-x-2 pt-2">
                <Button size="sm" variant="outline" className="flex-1">
                  <Eye className="mr-2 h-3 w-3" />
                  View
                </Button>
                <Button size="sm" variant="outline" className="flex-1">
                  <Download className="mr-2 h-3 w-3" />
                  Download
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredDocuments.length === 0 && (
        <div className="text-center py-12">
          <p className="text-muted-foreground">No documents found matching your search.</p>
        </div>
      )}
    </div>
  )
}
