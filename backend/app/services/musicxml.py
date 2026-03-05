def is_valid(content: bytes) -> bool:
    """MusicXML 파일 기본 검증."""
    try:
        text = content.decode("utf-8")
        return "<score-partwise" in text or "<score-timewise" in text
    except Exception:
        return False
