"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Spinner } from "@/components/ui/spinner";
import { CommonAlert } from "@/components/common/alert";

const defaultSpec = {
    objective: "Allow users to create and view simple tasks",
    user_story:
        "As a user, I want to create tasks and view my task list so that I can track basic work items.",
    business_rules: [
        "A task title is required",
        "A task title cannot exceed 100 characters",
        "A task is created as incomplete by default",
    ],
    acceptance_criteria: [
        "User can create a task with a title",
        "User can view all created tasks",
        "System rejects a task with an empty title",
    ],
    non_functional_requirements: [
        "API responses should be returned quickly",
        "Input validation must be applied",
    ],
    out_of_scope: [
        "Authentication",
        "Task editing",
        "Task deletion",
        "Database persistence",
        "User-specific task ownership",
    ],
};

type AlertState = {
    type: "success" | "danger";
    title: string;
    description: string;
} | null;

type Props = {
    loadingAction: string | null;
    onCreatePipeline: (specText: string) => Promise<void>;
};

export function SpecInputCard({ loadingAction, onCreatePipeline }: Props) {
    const [specText, setSpecText] = useState(JSON.stringify(defaultSpec, null, 2));
    const [alert, setAlert] = useState<AlertState>(null);

    const isCreating = loadingAction === "create";

    async function handleCreatePipeline() {
        setAlert(null);

        let parsedSpec: typeof defaultSpec;

        try {
            parsedSpec = JSON.parse(specText);
        } catch {
            setAlert({
                type: "danger",
                title: "Invalid specification",
                description: "Input format is wrong. Please provide valid JSON.",
            });
            return;
        }

        try {
            await onCreatePipeline(specText);

            setAlert({
                type: "success",
                title: "Pipeline created",
                description: "The specification is validated and created",
            });
        } catch {
            setAlert({
                type: "danger",
                title: "Pipeline creation failed",
                description: "Unable to create the pipeline. Please check the input.",
            });
        }
    }

    return (
        <>
            <Card>
                <CardHeader>
                    <CardTitle>Feature Specification</CardTitle>
                </CardHeader>

                <CardContent className="space-y-4">
                    <Textarea
                        className="min-h-[420px] font-mono text-sm"
                        value={specText}
                        disabled={isCreating}
                        onChange={(event) => setSpecText(event.target.value)}
                    />

                    <Button
                        onClick={handleCreatePipeline}
                        disabled={loadingAction !== null}
                        className="gap-2"
                    >
                        {isCreating && <Spinner className="h-4 w-4" />}
                        {isCreating ? "Creating..." : "Create Pipeline"}
                    </Button>
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