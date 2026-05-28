export type QualityCheck = {
    command: string;
    exit_code: number;
    stdout: string;
    stderr: string;
    passed: boolean;
};

export type QualityResults = {
    overall_status: "passed" | "failed";
    checks: Record<string, QualityCheck>;
};

export type FeatureSpec = {
    objective: string;
    user_story: string;
    business_rules: string[];
    acceptance_criteria: string[];
    non_functional_requirements: string[];
    out_of_scope: string[];
};

export type PipelineState = {
    pipeline_id: string;
    current_stage: string;
    status: string;
    spec?: FeatureSpec;
    plan?: unknown;
    generated_code?: unknown;
    generated_tests?: unknown;
    quality_results?: QualityResults;
};