// import { useEffect, useState } from "react";
// import { getResult } from "../api/client";

// export function useJobPolling(jobId) {
//   const [result, setResult] = useState(null);
//   const [loading, setLoading] = useState(false);

//   useEffect(() => {
//     if (!jobId) return;

//     setLoading(true);
//     setResult(null);

//     const interval = setInterval(async () => {
//       try {
//         const data = await getResult(jobId);

//         if (data.status === "done") {
//           clearInterval(interval);
//           setResult(data);
//           setLoading(false);
//         }

//         if (data.status === "error") {
//           clearInterval(interval);
//           setLoading(false);
//           console.error("❌ Job failed:", data.error || "Unknown error");
//         }
//       } catch (err) {
//         console.error("Polling error:", err);
//       }
//     }, 2000);

//     return () => clearInterval(interval);
//   }, [jobId]);

//   return { result, loading };
// }


import { useEffect, useState } from "react";
import { getResult } from "../api/client";

// Hook for polling a single job ID
export function useJobPolling(jobId) {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!jobId) return;

    setLoading(true);
    setResult(null);

    const interval = setInterval(async () => {
      try {
        const data = await getResult(jobId);

        if (data.status === "done") {
          clearInterval(interval);
          setResult(data);
          setLoading(false);
        }

        if (data.status === "error") {
          clearInterval(interval);
          setLoading(false);
          console.error("❌ Job failed:", data.error || "Unknown error");
        }
      } catch (err) {
        console.error("Polling error:", err);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [jobId]);

  return { result, loading };
}

// Standalone polling function for manual use (like in VideoUploader)
export async function pollJobResult(jobId, onResult) {
  const interval = setInterval(async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/result/${jobId}`);
      const data = await res.json();

      if (data.status === "done") {
        clearInterval(interval);
        onResult(data);
      }

      if (data.status === "error") {
        clearInterval(interval);
        console.error("❌ Job failed:", data.error || "Unknown error");
        onResult({ error: data.error });
      }
    } catch (err) {
      console.error("Polling error:", err);
    }
  }, 2000);

  return interval;
}