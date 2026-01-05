import Alert from './Alert';
import "../styles/AuditResults.css";
interface AuditResultsProps {
    result: {
        category: string;
        audit_report: string;
        form_prepared: boolean;
    } | null;
}

export default function AuditResults({result}: AuditResultsProps){
    if(!result){
        return null;
    }
    return(
        <div className = "results">
            <div className = "results-headers">
                <h2>Audit Results</h2>
                <span className="badge">category:{result.category}</span>
            </div>

        <div className = "report-content">
            {result.audit_report}
        </div>
        {result.form_prepared && (
            <Alert 
                type = "success"
                icon = "✅"
                message="ax form prepared and ready for filing"
            />
        )}
        </div>
    );
}


