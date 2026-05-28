"use client";

import { AlertCircle, CheckCircle2, X } from "lucide-react";

import {
    Alert,
    AlertDescription,
    AlertTitle,
} from "@/components/ui/alert";
import { Button } from "@/components/ui/button";

type CommonAlertProps = {
    type: "success" | "danger";
    title: string;
    description: string;
    onClose?: () => void;
};

export function CommonAlert({
    type,
    title,
    description,
    onClose,
}: CommonAlertProps) {
    const isDanger = type === "danger";

    return (
        <div className="fixed bottom-6 right-6 z-50 w-[380px]">
            <Alert
                variant={isDanger ? "destructive" : "default"}
                className="relative shadow-lg"
            >
                {isDanger ? (
                    <AlertCircle className="h-4 w-4" />
                ) : (
                    <CheckCircle2 className="h-4 w-4" />
                )}

                <div className="pr-8">
                    <AlertTitle>{title}</AlertTitle>
                    <AlertDescription className="wrap-break-word">
                        {description}
                    </AlertDescription>
                </div>

                {onClose && (
                    <Button
                        variant="ghost"
                        size="icon"
                        className="absolute right-2 top-2 h-6 w-6"
                        onClick={onClose}
                    >
                        <X className="h-4 w-4" />
                    </Button>
                )}
            </Alert>
        </div>
    );
}