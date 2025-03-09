import { CTABox } from '../../components/ctabox/ctabox'
import {
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
import { HowContent, HowWrapper } from './how.styles'

const scenarios = [
    {
        command: (
            <>
                pip install <PrimaryHighlight>helm-inspect</PrimaryHighlight>
            </>
        ),
        message: (
            <DullHighlight>
                Install HelmInspect, requiring only a single command.
            </DullHighlight>
        ),
    },
    {
        command: (
            <>
                helm-inspect -r myrelease -n mynamespace{' '}
                <PrimaryHighlight>--calibrate</PrimaryHighlight>
            </>
        ),
        message: (
            <DullHighlight>
                Analyzed 5 resources and found 22 drift-prone keys.
                <br />
                [INFO] Calibration data saved successfully.
            </DullHighlight>
        ),
    },
    {
        command: <>helm-inspect -r myrelease -n mynamespace</>,
        message: (
            <DullHighlight>
                [INFO] Checking drift for ConfigMap...
                <br />
                [ERROR] ❌ Drift detected in ConfigMap
                <br />
                @@ -1,3 +1,3 @@
                <br /> &#10100; <br />- "base.url": "anpan.xyz"
                <br />+ "base.url": "http://anpan.xyz"
                <br /> &#10101;
            </DullHighlight>
        ),
    },
]

export const How = () => {
    return (
        <HeroSection id="how-it-works">
            <HeroContentWrapper>
                <HowWrapper>
                    <HeroTitle>
                        How <PrimaryHighlight>It Works</PrimaryHighlight>
                    </HeroTitle>
                    <HowContent>
                        <CTABox
                            CTAText="Check The Docs!"
                            CTALink="https://github.com/qreater/HelmInspect?tab=readme-ov-file#table-of-contents"
                            CTANewTab
                            CTALeft
                        >
                            <HeroText>
                                With HelmInspect, you can catch and fix drifts
                                before they break your apps.
                            </HeroText>
                            <HeroList>
                                <HeroListItem>
                                    <PrimaryHighlight>
                                        Install & Run HelmInspect
                                    </PrimaryHighlight>
                                    .
                                </HeroListItem>
                                <MobileTrim>
                                    <HeroListItem>
                                        <PrimaryHighlight>
                                            Calibration
                                        </PrimaryHighlight>
                                        <HeroList>
                                            <HeroListItem>
                                                Kubernetes automatically adds
                                                system-generated keys, which
                                                should not be flagged as drift.
                                                HelmInspect solves this with
                                                calibration
                                            </HeroListItem>
                                        </HeroList>
                                    </HeroListItem>
                                </MobileTrim>
                                <HeroListItem>
                                    <PrimaryHighlight>
                                        Detecting Drift & Generating Reports.
                                    </PrimaryHighlight>
                                    <HeroList>
                                        <HeroListItem>
                                            <SecondaryHighlight>
                                                CLI output
                                            </SecondaryHighlight>{' '}
                                            highlights all drifted
                                            configurations.
                                        </HeroListItem>
                                        <HeroListItem>
                                            JSON report is automatically stored
                                            for tracking.
                                        </HeroListItem>
                                        <HeroListItem>
                                            Want{' '}
                                            <SecondaryHighlight>
                                                Slack alerts
                                            </SecondaryHighlight>
                                            ? Use --slack-token and
                                            --slack-channel to get a detailed
                                            report and logs, directly for your
                                            teams!
                                        </HeroListItem>
                                    </HeroList>
                                </HeroListItem>
                            </HeroList>
                        </CTABox>
                        <AnimatedScenarioBox
                            scenarios={scenarios}
                            intervalTime={4000}
                        />
                    </HowContent>
                </HowWrapper>
            </HeroContentWrapper>
        </HeroSection>
    )
}
