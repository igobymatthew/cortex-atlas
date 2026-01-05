export type AnalysisRequest = {
  subject_id: string;
  documents: Array<{
    document_id: string;
    author_id: string;
    source?: string;
    content: string;
    timestamp: string;
  }>;
  options?: {
    language?: string;
    retain_raw_text?: boolean;
    confidence_threshold?: number;
  };
};

export async function createAnalysis(request: AnalysisRequest) {
  const response = await fetch("/api/v1/analysis", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error("Failed to create analysis job.");
  }

  return response.json();
}

export async function fetchReport(analysisId: string) {
  const response = await fetch(`/api/v1/reports/${analysisId}`);
  if (!response.ok) {
    throw new Error("Report not available.");
  }
  return response.json();
}
