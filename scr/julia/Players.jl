module Players

    export AbstractPlayer, RandomPlayer, make_move!, place_pips!

    abstract type AbstractPlayer end

    struct RandomPlayer <: AbstractPlayer end

    function make_move!(p::AbstractPlayer,
                    mystate::Array{Array{Array{Int64,1},1},1},
                    oppstate::Array{Array{Array{Int64,1},1},1},
                    myscore::Int64,
                    oppscore::Int64,
                    myplace::Array{Tuple{Int64,Int64,Int64}},
                    oppplace::Array{Tuple{Int64,Int64,Int64}},
                    turn::Int64,
                    len::Int64,
                    npips::Int64)
        return (rand(1:3),rand(1:3),rand(1:3))
    end

    function place_pips!(p::AbstractPlayer,
                        v::Vector{Tuple{Int64,Int64,Int64}},
                        mystate::Array{Array{Array{Int64,1},1},1},
                        oppstate::Array{Array{Array{Int64,1},1},1},
                        myscore::Int64,
                        oppscore::Int64,
                        mymove::Tuple{Int64,Int64,Int64},
                        oppmove::Tuple{Int64,Int64,Int64},
                        turn::Int64,
                        len::Int64,
                        npips::Int64)
        for i in 1:length(v)
            v[i] = (rand(1:3),rand(1:3),rand(1:3))
        end
        return
    end

end  # module Players
