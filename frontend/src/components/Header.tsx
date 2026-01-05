import "../styles/Header.css";

export default function Header(){
    return(
        <header className = "header">
            <div className = "container">
                <div className="header-content">
                    <div className = "logo">
                        <div className = "logo-icon">📊</div>
                            <div className = "logo-text">
                                <h1>Fiscalpulse</h1>
                                <p>Autonomous AI Audit Agent</p>
                            </div>
                    </div>
                </div>
            </div>
        </header>
    )
}