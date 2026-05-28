"use client";

import { useState } from "react";
import { FileText, CheckCircle2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Spinner } from "@/components/ui/spinner";
import type { PipelineState } from "@/lib/types";
import { CommonAlert } from "@/components/common/alert";

type AlertState = {
    type: "success" | "danger";
    title: string;
    description: string;
} | null;

type Props = {
    pipeline: PipelineState | null;
    loadingAction: string | null;
    onGeneratePlan: () => Promise<void>;
    onApprovePlan: (onProgress?: (message: string) => void) => Promise<void>;
};

export function PipelineActionsCard({
    pipeline,
    loadingAction,
    onGeneratePlan,
    onApprovePlan,
}: Props) {
    const [alert, setAlert] = useState<AlertState>(null);
    const [progressMessage, setProgressMessage] = useState<string | null>(null);

    const isGeneratingPlan = loadingAction === "plan";
    const isApprovingPlan = loadingAction === "approve";

    const hasPipeline = Boolean(pipeline);
    const hasPlan = Boolean(pipeline?.plan);
    const hasGeneratedCode = Boolean(pipeline?.generated_code);

    const canGeneratePlan =
        hasPipeline &&
        !hasPlan &&
        loadingAction === null;

    const canApprovePlan =
        hasPipeline &&
        hasPlan &&
        !hasGeneratedCode &&
        loadingAction === null;

    async function handleGeneratePlan() {
        setAlert(null);
        setProgressMessage(null);

        try {
            await onGeneratePlan();

            setAlert({
                type: "success",
                title: "Plan generated",
                description: "The implementation plan was generated successfully.",
            });
        } catch {
            setAlert({
                type: "danger",
                title: "Plan generation failed",
                description: "Unable to generate the implementation plan.",
            });
        }
    }

    async function handleApprovePlan() {
        setAlert(null);
        setProgressMessage(null);

        try {
            await onApprovePlan((message) => {
                setProgressMessage(message);
            });

            setAlert({
                type: "success",
                title: "Pipeline automation completed",
                description:
                    "Plan approved, code saved, tests generated, and quality checks completed.",
            });
        } catch {
            setAlert({
                type: "danger",
                title: "Pipeline automation failed",
                description:
                    "Something failed while approving, generating code, saving files, or running tests.",
            });
        }
    }

    return (
        <>
            <Card>
                <CardHeader>
                    <CardTitle>Actions</CardTitle>
                </CardHeader>

                <CardContent className="space-y-3">
                    <Button
                        className="w-full justify-start gap-2"
                        onClick={handleGeneratePlan}
                        disabled={!canGeneratePlan}
                    >
                        {isGeneratingPlan ? (
                            <Spinner className="h-4 w-4" />
                        ) : (
                            <FileText className="h-4 w-4" />
                        )}

                        {isGeneratingPlan ? "Generating plan..." : "Generate Plan"}
                    </Button>

                    <Button
                        className="w-full justify-start gap-2"
                        onClick={handleApprovePlan}
                        disabled={!canApprovePlan}
                    >
                        {isApprovingPlan ? (
                            <Spinner className="h-4 w-4" />
                        ) : (
                            <CheckCircle2 className="h-4 w-4" />
                        )}

                        {hasGeneratedCode
                            ? "Pipeline Generated"
                            : isApprovingPlan
                                ? "Running pipeline..."
                                : "Approve Plan"}
                    </Button>

                    {progressMessage && (
                        <p className="text-xs text-muted-foreground">
                            {progressMessage}
                        </p>
                    )}

                    {!pipeline && (
                        <p className="text-xs text-muted-foreground">
                            Create a pipeline before running actions.
                        </p>
                    )}

                    {pipeline && !hasPlan && (
                        <p className="text-xs text-muted-foreground">
                            Generate a plan from the uploaded specification.
                        </p>
                    )}

                    {hasPlan && !hasGeneratedCode && (
                        <p className="text-xs text-muted-foreground">
                            Approving the plan will generate code, save files, generate tests,
                            and run quality checks.
                        </p>
                    )}

                    {hasGeneratedCode && (
                        <p className="text-xs text-green-600">
                            Code generated and saved. Check the generated folder.
                        </p>
                    )}
                </CardContent>
            </Card>

            {alert && (
                <CommonAlert
                    type={alert.type}
                    title={alert.title}
                    description={alert.description}
                    onClose={() => setAlert(null)}
                />
            )}
        </>
    );
}