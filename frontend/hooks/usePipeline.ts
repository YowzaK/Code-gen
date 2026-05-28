"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import type { PipelineState, QualityResults } from "@/lib/types";

export function usePipeline() {
    const [pipeline, setPipeline] = useState<PipelineState | null>(null);
    const [loadingAction, setLoadingAction] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [qualityResults, setQualityResults] = useState<QualityResults | null>(null);

    async function refreshPipeline(pipelineId: string) {
        const pipelineResponse = await api.get(`/pipeline/${pipelineId}`);
        setPipeline(pipelineResponse.data);

        if (pipelineResponse.data?.quality_results) {
            setQualityResults(pipelineResponse.data.quality_results);
        }

        return pipelineResponse.data;
    }

    async function runAction(action: string, callback: () => Promise<void>) {
        try {
            setError(null);
            setLoadingAction(action);
            await callback();
        } catch (err: any) {
            const detail = err?.response?.data?.detail;

            if (typeof detail === "string") {
                setError(detail);
            } else if (detail?.message) {
                setError(detail.message);
            } else {
                setError(err?.message || "Something went wrong");
            }

            throw err;
        } finally {
            setLoadingAction(null);
        }
    }

    async function createPipeline(specText: string) {
        await runAction("create", async () => {
            const parsedSpec = JSON.parse(specText);
            const response = await api.post("/spec/upload", parsedSpec);

            const pipelineId = response.data.data.pipeline_id;
            await refreshPipeline(pipelineId);
            setQualityResults(null);
        });
    }

    async function generatePlan() {
        if (!pipeline) return;

        await runAction("plan", async () => {
            await api.post(`/pipeline/${pipeline.pipeline_id}/plan`);
            await refreshPipeline(pipeline.pipeline_id);
        });
    }

    async function approvePlan(onProgress?: (message: string) => void) {
        if (!pipeline) return;

        await runAction("approve", async () => {
            onProgress?.("Approving implementation plan...");
            await api.post(`/pipeline/${pipeline.pipeline_id}/approve`);
            await refreshPipeline(pipeline.pipeline_id);

            onProgress?.("Generating code using AI...");
            await api.post(`/pipeline/${pipeline.pipeline_id}/generate-code`);
            await refreshPipeline(pipeline.pipeline_id);

            onProgress?.("Saving generated code files...");
            await api.post(`/pipeline/${pipeline.pipeline_id}/save-code`);
            await refreshPipeline(pipeline.pipeline_id);

            onProgress?.("Generating automated tests...");
            await api.post(`/pipeline/${pipeline.pipeline_id}/generate-tests`);
            await refreshPipeline(pipeline.pipeline_id);

            onProgress?.("Running quality checks...");

            try {
                const qualityResponse = await api.post(
                    `/pipeline/${pipeline.pipeline_id}/run-quality-check`
                );

                const results = qualityResponse.data?.quality_results;
                if (results) {
                    setQualityResults(results);
                }

                await refreshPipeline(pipeline.pipeline_id);
                onProgress?.("Quality checks completed.");
            } catch (err: any) {
                const qualityResultsFromError =
                    err?.response?.data?.detail?.quality_results;

                if (qualityResultsFromError) {
                    setQualityResults(qualityResultsFromError);
                }

                await refreshPipeline(pipeline.pipeline_id);

                onProgress?.("Quality checks completed with failures.");
            }
        });
    }

    return {
        pipeline,
        loadingAction,
        error,
        qualityResults,
        createPipeline,
        generatePlan,
        approvePlan,
    };
}