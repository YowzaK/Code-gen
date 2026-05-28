"use client";

import { usePipeline } from "@/hooks/usePipeline";
import { SpecInputCard } from "@/components/pipeline/SpecInputCard";
import { PipelineStatusCard } from "@/components/pipeline/PipeLineStatusCard";
import { PipelineActionsCard } from "@/components/pipeline/PipelineActionsCard";
import { QualityChecksCard } from "@/components/pipeline/QualityChecksCard";

export default function Home() {
  const {
    pipeline,
    loadingAction,
    qualityResults,
    createPipeline,
    generatePlan,
    approvePlan,
  } = usePipeline();

  return (
    <main className="min-h-screen bg-muted/30 p-6">
      <div className="mx-auto max-w-7xl space-y-6">
        <div>
          <h1 className="text-3xl font-bold">
            CodeGen an AI-Native Development Pipeline
          </h1>
          <p className="text-muted-foreground">
            Spec intake, planning, approval, code generation, tests, and quality
            gates.
          </p>
        </div>

        <div className="flex flex-col gap-6 xl:flex-row xl:items-start">
          <div className="xl:flex-[1.1]">
            <SpecInputCard
              loadingAction={loadingAction}
              onCreatePipeline={createPipeline}
            />
          </div>

          <div className="xl:flex-1">
            <PipelineStatusCard pipeline={pipeline} />
          </div>

          <div className="space-y-6 xl:flex-[0.9]">
            <PipelineActionsCard
              pipeline={pipeline}
              loadingAction={loadingAction}
              onGeneratePlan={generatePlan}
              onApprovePlan={approvePlan}
            />

            <QualityChecksCard qualityResults={qualityResults} />
          </div>
        </div>


      </div>
    </main>
  );
}