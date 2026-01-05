import FeatureCard from "./FeatureCard";

export default function Features(){
    const features = [
        {
            icon:"🔒",
            title:"Secure&Private",
            description:"All data stays local. Your financial information never leaves your system."
        },

        {
        icon: '⚡',
        title: 'AI-Powered',
        description: 'Uses advanced LLMs to understand tax rules and identify discrepancies.'
        },
        {
        icon: '⏱️',
        title: 'Real-Time Analysis',
        description: 'Get instant audit results and tax compliance checks on demand.'
        }
    ];

    return(
        <div className = "features">
            {features.map((feature,index)=>(
                <FeatureCard
                    key={index}
                    icon={feature.icon}
                    title={feature.title}
                    description={feature.description}
                />
            ))}
        </div>
    )
}