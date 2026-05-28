import { CheckCircle2, Circle } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { PipelineState } from "@/lib/types";

type Props = {
    pipeline: PipelineState | null;
};

const stages = [
    {
        label: "Specification uploaded",
        description: "Feature spec validated and stored",
        isDone: (pipeline: PipelineState | null) => Boolean(pipeline),
    },
    {
        label: "Plan generated",
        description: "AI generated implementation plan",
        isDone: (pipeline: PipelineState | null) => Boolean(pipeline?.plan),
    },
    {
        label: "Plan approved",
        description: "Human approval checkpoint completed",
        isDone: (pipeline: PipelineState | null) =>
            pipeline?.current_stage === "spec_plan_approved" ||
            Boolean(pipeline?.generated_code),

    },
    {
        label: "Code generated",
        description: "AI generated code artifacts",
        isDone: (pipeline: PipelineState | null) =>
            Boolean(pipeline?.generated_code),
    },
    {
        label: "Tests generated",
        description: "AI generated automated tests",
        isDone: (pipeline: PipelineState | null) =>
            Boolean(pipeline?.generated_tests),
    },
    {
        label: "Quality gates",
        description: "Linting, tests, security and policy checks",
        isDone: (pipeline: PipelineState | null) =>
            Boolean(pipeline?.quality_results),
    },
];

function getBadgeVariant(status?: string) {
    if (!status) return "secondary";

    if (status.includes("failed")) {
        return "destructive";
    }

    if (status.includes("passed") || status.includes("completed")) {
        return "default";
    }

    return "secondary";
}

export function PipelineStatusCard({ pipeline }: Props) {
    return (
        <Card>
            <CardHeader>
                <CardTitle>Pipeline Status</CardTitle>
            </CardHeader>

            <CardContent className="space-y-5">
                {pipeline ? (
                    <div className="space-y-3 rounded-lg border bg-muted/30 p-4">
                        <div className="space-y-1">
                            <p className="text-sm text-muted-foreground">
                                Pipeline ID
                            </p>
                            <p className="break-all font-mono text-sm">
                                {pipeline.pipeline_id}
                            </p>
                        </div>

                        <div className="flex flex-wrap gap-2">
                            <Badge variant="outline">
                                {pipeline.current_stage}
                            </Badge>
                            <Badge variant={getBadgeVariant(pipeline.status)}>
                                {pipeline.status}
                            </Badge>
                        </div>
                    </div>
                ) : (
                    <div className="rounded-lg border border-dashed p-4 text-sm text-muted-foreground">
                        No pipeline created yet. Submit a specification to begin.
                    </div>
                )}

                <div className="space-y-4">
                    {stages.map((stage) => {
                        const done = stage.isDone(pipeline);

                        return (
                            <div key={stage.label} className="flex gap-3">
                                <div className="mt-1">
                                    {done ? (
                                        <CheckCircle2 className="h-5 w-5 text-green-600" />
                                    ) : (
                                        <Circle className="h-5 w-5 text-muted-foreground" />
                                    )}
                                </div>

                                <div className="space-y-1">
                                    <p className="text-sm font-medium">
                                        {stage.label}
                                    </p>
                                    <p className="text-xs text-muted-foreground">
                                        {stage.description}
                                    </p>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </CardContent>
        </Card>
    );
}