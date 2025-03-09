import CommandBox from '../../components/commandbox/commandbox'
import {
    ButtonLink,
    CodeParagraph,
    HeroContentWrapper,
    HeroSection,
    HeroText,
    HeroTitle,
    MobileTrim,
    PrimaryHighlight,
    SecondaryHighlight,
} from '../../components/index.styles'
import { LandingContent } from './landing.styles'

export const Landing = () => {
    const scrollToWhy = (
        e: React.MouseEvent<HTMLAnchorElement, MouseEvent>,
    ) => {
        e.preventDefault()
        document.getElementById('why-helm-inspect')?.scrollIntoView({
            behavior: 'smooth',
            block: 'start',
        })
    }

    return (
        <HeroSection>
            <HeroContentWrapper>
                <LandingContent>
                    <HeroTitle>
                        Detect Helm Drift{' '}
                        <PrimaryHighlight>Instantly</PrimaryHighlight>.{' '}
                        <PrimaryHighlight>No Setup</PrimaryHighlight> Required.
                    </HeroTitle>
                    <HeroText>
                        <MobileTrim>
                            Manually{' '}
                            <PrimaryHighlight>
                                modified Kubernetes
                            </PrimaryHighlight>{' '}
                            resources can lead to inconsistencies, downtime, and
                            security risks.{' '}
                        </MobileTrim>
                        <SecondaryHighlight>Helm Inspect</SecondaryHighlight>{' '}
                        helps you track and detect{' '}
                        <PrimaryHighlight>drift</PrimaryHighlight> between your
                        Helm manifests and the actual deployed resources
                        <MobileTrim>
                            —<PrimaryHighlight>without</PrimaryHighlight> any
                            complicated setup.
                        </MobileTrim>
                    </HeroText>
                    <CommandBox copyText="pip install helm-inspect">
                        <CodeParagraph>
                            pip install{' '}
                            <PrimaryHighlight>helm-inspect</PrimaryHighlight>
                        </CodeParagraph>
                    </CommandBox>
                    <ButtonLink href="#why-helm-inspect" onClick={scrollToWhy}>
                        Why Helm Inspect?
                    </ButtonLink>
                </LandingContent>
            </HeroContentWrapper>
        </HeroSection>
    )
}
