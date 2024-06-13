def state_to_binary(save_id: int,
                    components: list[dict],
                    wires: list[dict],
                    gate: int,
                    delay: int,
                    menu_visible: bool,
                    clock_speed: int,
                    description: str,
                    camera_position: dict,
                    hub_id: int,
                    hub_description: str,
                    synced: int = ...,
                    campaign_bound: bool = ...,
                    player_data: bytes = ...) \
        -> bytes: ...


def parse_state(input: bytes, headers_only: bool = ..., solution: bool = ...) \
        -> dict: ...
