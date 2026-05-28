import { CheckCircle2, XCircle } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { QualityResults } from "@/lib/types";

type Props = {
    qualityResults: QualityResults | null;
};

function formatCheckName(name: string) {
    return name
        .replaceAll("_", " ")
        .replace(/\b\w/g, (char) => char.toUpperCase());
}

export function QualityChecksCard({ qualityResults }: Props) {
    if (!qualityResults) {
        return null;
    }

    const checks = Object.entries(qualityResults.checks ?? {});

    const passedCount = checks.filter(([, check]) => check.passed).length;
    const failedCount = checks.filter(([, check]) => !check.passed).length;

    return (
        <Card>
            <CardHeader>
                <CardTitle>Quality Checks</CardTitle>
            </CardHeader>

            <CardContent className="space-y-4">
                <div className="flex flex-wrap gap-2">
                    <Badge
                        variant={
                            qualityResults.overall_status === "passed"
                                ? "default"
                                : "destructive"
                        }
                    >
                        {qualityResults.overall_status}
                    </Badge>

                    <Badge variant="outline">{passedCount} passed</Badge>
                    <Badge variant="outline">{failedCount} failed</Badge>
                </div>

                <div className="space-y-3">
                    {checks.map(([checkName, check]) => (
                        <div
                            key={checkName}
                            className="flex items-center justify-between rounded-lg border p-3"
                        >
                            <div className="flex items-center gap-2">
                                {check.passed ? (
                                    <CheckCircle2 className="h-4 w-4 text-green-600" />
                                ) : (
                                    <XCircle className="h-4 w-4 text-red-600" />
                                )}

                                <span className="text-sm font-medium">
                                    {formatCheckName(checkName)}
                                </span>
                            </div>

                            <Badge
                                variant={check.passed ? "default" : "destructive"}
                            >
                                {check.passed ? "Passed" : "Failed"}
                            </Badge>
                        </div>
                    ))}
                </div>
            </CardContent>
        </Card>
    );
}