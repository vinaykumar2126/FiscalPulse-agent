import "../styles/AuditForm.css";

interface AuditFormProps {
    query: string;
    setQuery: (query: string) => void;
    handleSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
    loading: boolean;
}

export default function AuditForm({query,setQuery,handleSubmit,loading}: AuditFormProps){
    return(
        <form onSubmit = {handleSubmit} className = "audit-form">
            <div className = "form-group">
                <label htmlFor="query">What would you like to audit today?</label>
                <textarea
                    id="query"
                    rows= {4}
                    placeholder="e.g., Check my hardware expenses for tax deductions"
                    value = {query}
                    onChange = {(e)=> setQuery(e.target.value)}
                    disabled = {loading}
                    required
                />
            </div>
            <button type = "submit" className = "btn-primary"
            disabled = {loading || !query.trim()}>
                {loading ? (
                    <>
                    <span className="loader"></span>
                    <span>Analyzing</span>
                    </>
                ):(
                    <span>🚀 Start Audit</span>
                )}

            </button>
        </form>
    )
}