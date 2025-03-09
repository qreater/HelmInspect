import { CTABox } from '../../components/ctabox/ctabox'
import {
    AccentHighlight,
    DullHighlight,
    HeroContentWrapper,
    HeroList,
    HeroListItem,
    HeroSection,
    HeroText,
    HeroTitle,
    MobileTrim,
    PrimaryHighlight,
    SecondaryHighlight,
} from '../../components/index.styles'
import AnimatedScenarioBox from '../../components/scenariobox/scenariobox'
import { WhyContent, WhyWrapper } from './why.styles'

const scenarios = [
    {
        time: '16:00:00',
        command: (
            <>
                helm <PrimaryHighlight>install</PrimaryHighlight>
            </>
        ),
        message: (
            <DullHighlight>
                Installation Succeeded on the production cluster.{' '}
                <MobileTrim>Running out tests on the environment.</MobileTrim>
            </DullHighlight>
        ),
    },
    {
        time: '16:20:00',
        command: <>Tests Fail; RCA On-Going</>,
        message: (
            <DullHighlight>
                <MobileTrim>Tests failed on the production cluster.</MobileTrim>{' '}
                The team is currently investigating the root cause.
            </DullHighlight>
        ),
    },
    {
        time: '16:30:00',
        command: <>Configurations Found to be Incorrect!</>,
        message: (
            <DullHighlight>
                One of the ConfigMap values is incorrect.
            </DullHighlight>
        ),
    },
    {
        time: '16:40:00',
        command: (
            <>
                kubectl <PrimaryHighlight>edit</PrimaryHighlight> cm -o yaml
            </>
        ),
        message: (
            <DullHighlight>
                <AccentHighlight>Manually</AccentHighlight> patching the
                ConfigMap to fix the issue.
            </DullHighlight>
        ),
    },
]

export const Why = () => {
    return (
        <HeroSection id="why-helm-inspect">
            <HeroContentWrapper>
                <WhyWrapper>
                    <HeroTitle>
                        Why <PrimaryHighlight>Helm Inspect</PrimaryHighlight>
                    </HeroTitle>
                    <WhyContent>
                        <AnimatedScenarioBox
                            scenarios={scenarios}
                            intervalTime={2000}
                        />
                        <CTABox CTAText="How it works?" CTALink="#how-it-works">
                            <HeroText>Helm Drift Occurs When,</HeroText>
                            <HeroList>
                                <HeroListItem>
                                    Kubernetes resources{' '}
                                    <AccentHighlight>
                                        are manually changed
                                    </AccentHighlight>{' '}
                                    instead of using helm{' '}
                                    <PrimaryHighlight>upgrade</PrimaryHighlight>
                                    .
                                </HeroListItem>
                                <MobileTrim>
                                    <HeroListItem>
                                        Configurations differ from what Helm
                                        originally deployed, causing hidden{' '}
                                        <PrimaryHighlight>
                                            inconsistencies
                                        </PrimaryHighlight>
                                        .
                                    </HeroListItem>
                                </MobileTrim>
                                <HeroListItem>
                                    Future upgrades fail due to unexpected
                                    changes in resource definitions.
                                </HeroListItem>
                            </HeroList>
                            <HeroText>
                                While ArgoCD can prevent drift in{' '}
                                <SecondaryHighlight>GitOps</SecondaryHighlight>{' '}
                                setups, not every system has it in place.
                            </HeroText>
                            <HeroText>
                                <PrimaryHighlight>HelmInspect</PrimaryHighlight>{' '}
                                is a lightweight CLI tool that instantly detects
                                drift, providing actionable insights without
                                requiring complex configurations.
                            </HeroText>
                        </CTABox>
                    </WhyContent>
                </WhyWrapper>
            </HeroContentWrapper>
        </HeroSection>
    )
}
