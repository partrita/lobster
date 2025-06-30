# Lobster 모델

## [범용 분자 인코더 (Universal Molecular Encoder)](_ume.py)
* UME는 `flash-attn`으로 학습됩니다. GPU에서 `flash-attn`을 사용하여 올바르게 실행하거나 CPU에서 `flash-attn` 없이 실행하도록 모델을 동적으로 구성하는 사용자 지정 `load_from_checkpoint` 메서드를 구현합니다.
